package academy.mentor;

import java.time.Duration;
import java.time.Instant;
import java.util.List;

/**
 * The mentor's escalation rules (docs/curriculum/04-ai-mentor-policy.md §2–§3), as pure functions
 * of the learner's history so they can be tested without a model or a database.
 */
public final class MentorPolicy {

    static final Duration WORKED_EXAMPLE_WAIT = Duration.ofMinutes(10);
    static final int SOLUTION_REQUESTS_TO_TRIGGER = 3;
    static final int RECENT_LEARNER_MESSAGES = 10;
    static final int RECENT_EXERCISES = 5;
    static final int HIGH_HELP_EXERCISES_TO_TRIGGER = 3;
    static final int INDEPENDENT_EXERCISES_TO_EXIT = 3;

    private MentorPolicy() {}

    /** One graded submission on this exercise: when, and a fingerprint of what was submitted. */
    public record AttemptFact(Instant at, String submissionHash) {}

    /** What has happened on this exercise so far. */
    public record ExerciseHistory(
            List<AttemptFact> attempts,
            Instant targetedHintGivenAt,
            Instant workedExampleGivenAt) {}

    public record Gate(boolean allowed, boolean needsConfirmation, String reason) {

        static Gate allow() {
            return new Gate(true, false, null);
        }

        static Gate deny(String reason) {
            return new Gate(false, false, reason);
        }

        static Gate confirm(String reason) {
            return new Gate(false, true, reason);
        }
    }

    /**
     * Whether the learner may receive help at {@code target}.
     *
     * @param cap the highest level allowed in this context (H1 in knowledge checks)
     * @param attemptFirst whether attempt-first mode is active for this learner
     * @param hypothesis the learner's one-sentence guess at what's wrong, required for H2+ in attempt-first mode
     */
    public static Gate gate(MentorLevel target, MentorLevel cap, ExerciseHistory history, boolean attemptFirst,
            String hypothesis, boolean confirmedWalkthrough, Instant now) {
        if (target.compareTo(cap) > 0) {
            return Gate.deny(cap == MentorLevel.NUDGE
                    ? "In a knowledge check the mentor can only give nudges. That keeps the check a fair test of what you remember."
                    : "This is as much help as is available here.");
        }
        if (target.compareTo(MentorLevel.TARGETED_HINT) < 0) {
            return Gate.allow();
        }
        if (attemptFirst && (hypothesis == null || hypothesis.isBlank())) {
            return Gate.deny("First, tell the mentor in one sentence what you think is going wrong.");
        }
        return switch (target) {
            case TARGETED_HINT -> history.attempts().isEmpty()
                    ? Gate.deny("Check your code against the tests at least once to unlock a targeted hint.")
                    : Gate.allow();
            case WORKED_EXAMPLE -> {
                if (history.targetedHintGivenAt() == null) {
                    yield Gate.deny("Ask for a targeted hint first.");
                }
                long changedAttempts = history.attempts().stream()
                        .filter(a -> a.at().isAfter(history.targetedHintGivenAt()))
                        .map(AttemptFact::submissionHash).distinct().count();
                boolean waited = !now.isBefore(history.targetedHintGivenAt().plus(WORKED_EXAMPLE_WAIT));
                yield changedAttempts >= 2 || waited
                        ? Gate.allow()
                        : Gate.deny("Try the hint: check two changed versions of your code (or keep working for 10 minutes) to unlock a worked example.");
            }
            case WALKTHROUGH -> {
                if (history.workedExampleGivenAt() == null) {
                    yield Gate.deny("Ask for a worked example first.");
                }
                boolean triedSince = history.attempts().stream().anyMatch(a -> a.at().isAfter(history.workedExampleGivenAt()));
                if (!triedSince) {
                    yield Gate.deny("Try once more using the worked example to unlock a walkthrough.");
                }
                yield confirmedWalkthrough
                        ? Gate.allow()
                        : Gate.confirm("After a walkthrough, this exercise won't count towards independent mastery. "
                                + "We'll give you a similar one later so you can show you've got it.");
            }
            default -> Gate.allow();
        };
    }

    /** One message in a learner's mentor history, across all exercises, oldest first. */
    public record MentorEvent(Instant at, String exerciseId, boolean fromLearner, boolean solutionRequest, int level) {}

    /** A passing attempt: when, on which exercise, and whether it counted as independent. */
    public record Pass(Instant at, String exerciseId, boolean independent) {}

    /**
     * Whether attempt-first mode is active (policy §3): several recent messages asking outright for
     * solutions, or worked examples/walkthroughs on most recent exercises. It ends once the learner
     * passes three different exercises with no more than a nudge.
     */
    public static boolean attemptFirst(List<MentorEvent> events, List<Pass> passes) {
        Instant triggeredAt = null;

        List<MentorEvent> learnerMessages = events.stream().filter(MentorEvent::fromLearner).toList();
        List<MentorEvent> recent = learnerMessages.subList(
                Math.max(0, learnerMessages.size() - RECENT_LEARNER_MESSAGES), learnerMessages.size());
        List<MentorEvent> requests = recent.stream().filter(MentorEvent::solutionRequest).toList();
        if (requests.size() >= SOLUTION_REQUESTS_TO_TRIGGER) {
            triggeredAt = requests.getLast().at();
        }

        List<String> exercises = events.stream().map(MentorEvent::exerciseId).distinct().toList();
        List<String> recentExercises = exercises.subList(Math.max(0, exercises.size() - RECENT_EXERCISES), exercises.size());
        List<MentorEvent> highHelp = events.stream()
                .filter(e -> !e.fromLearner() && e.level() >= MentorLevel.WORKED_EXAMPLE.number())
                .filter(e -> recentExercises.contains(e.exerciseId()))
                .toList();
        if (highHelp.stream().map(MentorEvent::exerciseId).distinct().count() >= HIGH_HELP_EXERCISES_TO_TRIGGER) {
            Instant last = highHelp.getLast().at();
            triggeredAt = triggeredAt == null || last.isAfter(triggeredAt) ? last : triggeredAt;
        }

        if (triggeredAt == null) {
            return false;
        }
        Instant since = triggeredAt;
        long independentExercises = passes.stream()
                .filter(p -> p.independent() && p.at().isAfter(since))
                .map(Pass::exerciseId)
                .distinct()
                .count();
        return independentExercises < INDEPENDENT_EXERCISES_TO_EXIT;
    }
}
