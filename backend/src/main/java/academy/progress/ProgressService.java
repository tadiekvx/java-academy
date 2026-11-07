package academy.progress;

import java.time.Clock;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import academy.assessment.GradeReport;
import academy.assessment.Submission;
import academy.content.Concept;
import academy.content.Content;
import academy.content.ContentRepository;
import academy.content.Evidence;
import academy.content.Exercise;
import academy.content.ExerciseType;
import academy.progress.MasteryCalculator.ConceptMastery;
import tools.jackson.databind.json.JsonMapper;

/** Records what learners do and derives their progress from it. */
@Service
public class ProgressService {

    /** The highest assistance level that still counts as independent work (H1, a conceptual nudge). */
    static final int MAX_INDEPENDENT_ASSISTANCE = 1;

    private final ContentRepository contentRepository;
    private final AttemptRepository attempts;
    private final LessonVisitRepository visits;
    private final ExplanationScoreRepository explanationScores;
    private final JsonMapper json;
    private final Clock clock;

    ProgressService(ContentRepository contentRepository, AttemptRepository attempts, LessonVisitRepository visits,
            ExplanationScoreRepository explanationScores, JsonMapper json, Clock clock) {
        this.contentRepository = contentRepository;
        this.attempts = attempts;
        this.visits = visits;
        this.explanationScores = explanationScores;
        this.json = json;
        this.clock = clock;
    }

    public void recordVisit(long learnerId, String lessonId) {
        visits.record(learnerId, lessonId, clock.instant());
    }

    /** Records an attempt and returns its id. */
    public long recordAttempt(long learnerId, Exercise exercise, Submission submission, GradeReport report,
            AttemptContext context, int assistanceLevel, boolean solutionViewed) {
        return attempts.record(learnerId, exercise.id(), clock.instant(), context, report, assistanceLevel, solutionViewed,
                json.writeValueAsString(submission));
    }

    /** The learner's attempts, oldest first. */
    public List<Attempt> attempts(long learnerId) {
        return attempts.forLearner(learnerId);
    }

    /**
     * Whether an attempt passed. An explanation (graded PENDING_REVIEW) passes once it has been
     * scored 2 out of 2.
     */
    public boolean passed(Attempt attempt, Map<Long, Integer> scores) {
        return attempt.passed() || (attempt.outcome() == GradeReport.Outcome.PENDING_REVIEW && scores.getOrDefault(attempt.id(), -1) == 2);
    }

    private static boolean awaitingReview(Attempt attempt, Map<Long, Integer> scores) {
        return attempt.outcome() == GradeReport.Outcome.PENDING_REVIEW && !scores.containsKey(attempt.id());
    }

    public Map<Long, Integer> explanationScores(long learnerId) {
        return explanationScores.forLearner(learnerId);
    }

    /** Concept names and mastery levels, for the mentor's context. */
    public Map<String, String> conceptLevels(long learnerId) {
        Map<String, String> levels = new LinkedHashMap<>();
        Content content = contentRepository.content();
        mastery(learnerId).forEach((id, m) -> levels.put(
                content.curriculum().concept(id).map(Concept::name).orElse(id), m.level().label()));
        return levels;
    }

    /**
     * @throws IllegalArgumentException if the exercise isn't currently a due retrieval check for the learner
     */
    public void requireDueCheck(long learnerId, String exerciseId) {
        boolean due = dueChecks(learnerId).stream().anyMatch(check -> check.exerciseId().equals(exerciseId));
        if (!due) {
            throw new IllegalArgumentException("That knowledge check isn't due right now.");
        }
    }

    public record ConceptView(
            String id,
            String name,
            int level,
            String levelName,
            int independentExercises,
            int assistedOnlyExercises,
            List<EvidenceView> evidence,
            Instant nextCheckDue) {}

    public record EvidenceView(Evidence type, String label, MasteryCalculator.Coverage coverage) {}

    public record DueCheck(String exerciseId, String title, List<String> conceptNames, Instant dueSince) {}

    public record LessonRef(String id, String title) {}

    public record ProgressView(List<ConceptView> concepts, List<DueCheck> dueChecks, LessonRef recommended) {}

    public record ExerciseStatus(int attempts, boolean passed, boolean passedIndependently, boolean pendingReview) {}

    public ProgressView progress(long learnerId) {
        Content content = contentRepository.content();
        Map<String, ConceptMastery> mastery = mastery(learnerId);
        List<ConceptView> concepts = content.curriculum().concepts().stream().map(concept -> {
            ConceptMastery m = mastery.get(concept.id());
            return new ConceptView(concept.id(), concept.name(), m.level().ordinal(), m.level().label(),
                    m.independentExercises(), m.assistedOnlyExercises(),
                    m.evidence().entrySet().stream()
                            .map(e -> new EvidenceView(e.getKey(), label(e.getKey()), e.getValue())).toList(),
                    m.nextCheckDue());
        }).toList();
        return new ProgressView(concepts, dueChecks(learnerId, mastery), recommend(mastery, visits.visitedLessons(learnerId)).orElse(null));
    }

    /** Per-exercise status for one lesson's exercises. */
    public Map<String, ExerciseStatus> lessonStatus(long learnerId, String lessonId) {
        Content content = contentRepository.content();
        Map<String, List<Attempt>> byExercise = attempts.forLearner(learnerId).stream()
                .collect(Collectors.groupingBy(Attempt::exerciseId));
        Map<Long, Integer> scores = explanationScores.forLearner(learnerId);
        Map<String, ExerciseStatus> statuses = new LinkedHashMap<>();
        for (Exercise exercise : content.exercises().values()) {
            if (!lessonId.equals(exercise.spec().lesson())) {
                continue;
            }
            List<Attempt> history = byExercise.getOrDefault(exercise.id(), List.of());
            boolean independent = false;
            for (int i = 0; i < history.size(); i++) {
                independent |= passed(history.get(i), scores) && isIndependent(exercise, history.get(i), i == 0);
            }
            statuses.put(exercise.id(), new ExerciseStatus(history.size(),
                    history.stream().anyMatch(a -> passed(a, scores)), independent,
                    history.stream().anyMatch(a -> awaitingReview(a, scores))));
        }
        return statuses;
    }

    /** Per-milestone status for one project: attempts so far, and whether it has been passed on one's own. */
    public Map<String, ExerciseStatus> projectStatus(long learnerId, academy.content.Project project) {
        Map<String, List<Attempt>> byExercise = attempts.forLearner(learnerId).stream()
                .collect(Collectors.groupingBy(Attempt::exerciseId));
        Map<String, ExerciseStatus> statuses = new LinkedHashMap<>();
        for (academy.content.Project.Milestone milestone : project.spec().milestones()) {
            String id = academy.content.Project.milestoneExerciseId(project.id(), milestone.id());
            List<Attempt> history = byExercise.getOrDefault(id, List.of());
            boolean passed = history.stream().anyMatch(Attempt::passed);
            boolean independent = history.stream().anyMatch(a -> a.passed()
                    && a.assistanceLevel() <= MAX_INDEPENDENT_ASSISTANCE && !a.solutionViewed());
            statuses.put(milestone.id(), new ExerciseStatus(history.size(), passed, independent, false));
        }
        return statuses;
    }

    public List<DueCheck> dueChecks(long learnerId) {
        return dueChecks(learnerId, mastery(learnerId));
    }

    Map<String, ConceptMastery> mastery(long learnerId) {
        Content content = contentRepository.content();
        List<Attempt> history = attempts.forLearner(learnerId);
        Map<Long, Integer> scores = explanationScores.forLearner(learnerId);
        Set<String> visited = visits.visitedLessons(learnerId);

        Map<String, List<MasteryCalculator.Event>> events = new HashMap<>();
        Set<String> seenExercises = new java.util.HashSet<>();
        for (Attempt attempt : history) {
            Optional<Exercise> found = content.exerciseOrMilestone(attempt.exerciseId());
            boolean first = seenExercises.add(attempt.exerciseId());
            if (found.isEmpty()) {
                continue; // The exercise has since been removed from the content.
            }
            Exercise exercise = found.get();
            var event = new MasteryCalculator.Event(attempt.submittedAt(), exercise.id(), Set.copyOf(exercise.spec().evidence()),
                    passed(attempt, scores), isIndependent(exercise, attempt, first), attempt.context() == AttemptContext.RETRIEVAL,
                    awaitingReview(attempt, scores));
            for (String concept : exercise.spec().concepts()) {
                events.computeIfAbsent(concept, c -> new ArrayList<>()).add(event);
            }
        }

        Map<String, ConceptMastery> result = new LinkedHashMap<>();
        for (Concept concept : content.curriculum().concepts()) {
            boolean introduced = content.lessons().values().stream()
                    .anyMatch(l -> visited.contains(l.id()) && l.meta().concepts().contains(concept.id()));
            result.put(concept.id(), MasteryCalculator.compute(concept.requiredEvidence(),
                    events.getOrDefault(concept.id(), List.of()), introduced));
        }
        return result;
    }

    /**
     * Whether a passing attempt counts as independent evidence: little or no help, no solution
     * viewed, not a Parsons problem (a scaffold), and for predict exercises only the first attempt,
     * because after that the learner has seen the real output.
     */
    static boolean isIndependent(Exercise exercise, Attempt attempt, boolean firstAttemptOnExercise) {
        if (attempt.assistanceLevel() > MAX_INDEPENDENT_ASSISTANCE || attempt.solutionViewed()) {
            return false;
        }
        if (exercise.type() == ExerciseType.PARSONS) {
            return false;
        }
        return exercise.type() != ExerciseType.PREDICT || firstAttemptOnExercise;
    }

    private List<DueCheck> dueChecks(long learnerId, Map<String, ConceptMastery> mastery) {
        Content content = contentRepository.content();
        Instant now = clock.instant();
        Map<String, Instant> lastAttempted = new HashMap<>();
        for (Attempt attempt : attempts.forLearner(learnerId)) {
            lastAttempted.put(attempt.exerciseId(), attempt.submittedAt());
        }

        Map<String, DueCheck> checks = new LinkedHashMap<>();
        for (Concept concept : content.curriculum().concepts()) {
            ConceptMastery m = mastery.get(concept.id());
            if (!m.checkDue(now)) {
                continue;
            }
            // Prefer variants the learner has never seen, then the one seen longest ago.
            content.exercises().values().stream()
                    .filter(e -> e.spec().role() == Exercise.Role.RETRIEVAL)
                    .filter(e -> e.spec().concepts().contains(concept.id()))
                    .filter(contentRepository::isAvailable)
                    .min(Comparator.comparing((Exercise e) -> lastAttempted.getOrDefault(e.id(), Instant.MIN))
                            .thenComparing(Exercise::id))
                    .ifPresent(exercise -> checks.merge(exercise.id(),
                            new DueCheck(exercise.id(), exercise.spec().title(), List.of(concept.name()), m.nextCheckDue()),
                            (a, b) -> new DueCheck(a.exerciseId(), a.title(),
                                    java.util.stream.Stream.concat(a.conceptNames().stream(), b.conceptNames().stream()).toList(),
                                    a.dueSince().isBefore(b.dueSince()) ? a.dueSince() : b.dueSince())));
        }
        return List.copyOf(checks.values());
    }

    /** The first available lesson, in curriculum order, that teaches a concept not yet Demonstrated. */
    private Optional<LessonRef> recommend(Map<String, ConceptMastery> mastery, Set<String> visited) {
        Content content = contentRepository.content();
        Set<String> skipped = new java.util.HashSet<>();
        content.curriculum().stages().stream().filter(academy.content.Curriculum.Stage::isOptional).forEach(stage -> {
            Set<String> ids = stage.modules().stream().flatMap(m -> m.lessons().stream())
                    .map(academy.content.Curriculum.LessonOutline::id).collect(Collectors.toSet());
            if (ids.stream().noneMatch(visited::contains)) {
                skipped.addAll(ids);
            }
        });
        return content.curriculum().lessonOutlines()
                .filter(outline -> !skipped.contains(outline.id()))
                .map(outline -> content.lesson(outline.id()).filter(contentRepository::isAvailable).orElse(null))
                .filter(java.util.Objects::nonNull)
                .filter(lesson -> lesson.meta().concepts().stream()
                        .anyMatch(c -> mastery.get(c).level().compareTo(MasteryLevel.DEMONSTRATED) < 0))
                .findFirst()
                .map(lesson -> new LessonRef(lesson.id(), lesson.meta().title()));
    }

    private static String label(Evidence type) {
        return switch (type) {
            case IMPL -> "Write it yourself";
            case EXPL -> "Explain it";
            case MIST -> "Spot the mistakes";
            case DEBUG -> "Debug it";
            case MOD -> "Change working code";
            case XFER -> "Use it on a new problem";
            case TRADE -> "Weigh the trade-offs";
        };
    }
}
