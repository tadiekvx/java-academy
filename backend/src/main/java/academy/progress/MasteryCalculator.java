package academy.progress;

import java.time.Duration;
import java.time.Instant;
import java.util.EnumMap;
import java.util.EnumSet;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import academy.content.Evidence;

/**
 * Computes one concept's mastery from the learner's history, replayed oldest first. Nothing is
 * stored: the level is always derived from the append-only attempt record.
 *
 * <p>Rules (docs/curriculum/01-curriculum-design.md §4):
 * <ul>
 *   <li>Practising: any passing attempt.</li>
 *   <li>Demonstrated: independent passes cover every required evidence type, across ≥ 2 exercises.</li>
 *   <li>Secure: Demonstrated, then an independent pass on a due retrieval check.</li>
 *   <li>Retained: three consecutive retrieval checks passed (the third comes ~30 days on).</li>
 *   <li>A failed check lowers the level by one (never below Demonstrated) and restarts the schedule.</li>
 * </ul>
 */
public final class MasteryCalculator {

    /** Gaps before the 1st, 2nd and 3rd retrieval checks; checks after that keep the last gap. */
    public static final List<Duration> CHECK_INTERVALS = List.of(Duration.ofDays(3), Duration.ofDays(10), Duration.ofDays(30));

    private static final int RETAINED_AFTER_CHECKS = 3;

    private MasteryCalculator() {}

    /** One graded attempt on an exercise that practises the concept. */
    public record Event(
            Instant time,
            String exerciseId,
            Set<Evidence> evidence,
            boolean passed,
            boolean independent,
            boolean retrieval,
            boolean pendingReview) {}

    public enum Coverage { INDEPENDENT, ASSISTED, PENDING_REVIEW, MISSING }

    public record ConceptMastery(
            MasteryLevel level,
            int independentExercises,
            int assistedOnlyExercises,
            Map<Evidence, Coverage> evidence,
            Instant demonstratedAt,
            Instant nextCheckDue) {

        public boolean checkDue(Instant now) {
            return nextCheckDue != null && !now.isBefore(nextCheckDue);
        }
    }

    public static ConceptMastery compute(List<Evidence> required, List<Event> events, boolean introduced) {
        Map<Evidence, Set<String>> independentCover = new EnumMap<>(Evidence.class);
        Set<Evidence> assistedCover = EnumSet.noneOf(Evidence.class);
        Set<Evidence> pendingCover = EnumSet.noneOf(Evidence.class);
        Set<String> independentExercises = new HashSet<>();
        Set<String> passedExercises = new HashSet<>();

        MasteryLevel level = MasteryLevel.NOT_STARTED;
        Instant demonstratedAt = null;
        Instant anchor = null;
        int checksPassed = 0;

        for (Event event : events) {
            if (event.pendingReview()) {
                pendingCover.addAll(event.evidence());
            }
            if (event.passed()) {
                passedExercises.add(event.exerciseId());
                if (event.independent()) {
                    independentExercises.add(event.exerciseId());
                    event.evidence().forEach(type -> independentCover.computeIfAbsent(type, t -> new HashSet<>()).add(event.exerciseId()));
                } else {
                    assistedCover.addAll(event.evidence());
                }
            }

            if (demonstratedAt == null) {
                if (requirementsMet(required, independentCover, independentExercises)) {
                    demonstratedAt = event.time();
                    anchor = event.time();
                    level = MasteryLevel.DEMONSTRATED;
                }
            } else if (event.retrieval() && !event.pendingReview()) {
                if (event.passed() && event.independent()) {
                    checksPassed = Math.min(checksPassed + 1, RETAINED_AFTER_CHECKS);
                    level = checksPassed >= RETAINED_AFTER_CHECKS ? MasteryLevel.RETAINED : max(level, MasteryLevel.SECURE);
                } else {
                    checksPassed = 0;
                    level = max(MasteryLevel.DEMONSTRATED, MasteryLevel.values()[level.ordinal() - 1]);
                }
                anchor = event.time();
            }
        }

        if (demonstratedAt == null) {
            level = !passedExercises.isEmpty() ? MasteryLevel.PRACTISING
                    : introduced || !events.isEmpty() ? MasteryLevel.INTRODUCED
                    : MasteryLevel.NOT_STARTED;
        }

        Map<Evidence, Coverage> coverage = new LinkedHashMap<>();
        for (Evidence type : required) {
            coverage.put(type, independentCover.containsKey(type) ? Coverage.INDEPENDENT
                    : assistedCover.contains(type) ? Coverage.ASSISTED
                    : pendingCover.contains(type) ? Coverage.PENDING_REVIEW
                    : Coverage.MISSING);
        }
        Set<String> assistedOnly = new HashSet<>(passedExercises);
        assistedOnly.removeAll(independentExercises);
        Instant nextCheckDue = anchor == null ? null
                : anchor.plus(CHECK_INTERVALS.get(Math.min(checksPassed, CHECK_INTERVALS.size() - 1)));
        return new ConceptMastery(level, independentExercises.size(), assistedOnly.size(), coverage, demonstratedAt, nextCheckDue);
    }

    private static boolean requirementsMet(List<Evidence> required, Map<Evidence, Set<String>> independentCover,
            Set<String> independentExercises) {
        return independentExercises.size() >= 2 && required.stream().allMatch(independentCover::containsKey);
    }

    private static MasteryLevel max(MasteryLevel a, MasteryLevel b) {
        return a.compareTo(b) >= 0 ? a : b;
    }
}
