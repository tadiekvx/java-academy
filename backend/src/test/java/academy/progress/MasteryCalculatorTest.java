package academy.progress;

import static academy.content.Evidence.DEBUG;
import static academy.content.Evidence.EXPL;
import static academy.content.Evidence.IMPL;
import static academy.content.Evidence.MIST;
import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import org.junit.jupiter.api.Test;

import academy.content.Evidence;
import academy.progress.MasteryCalculator.ConceptMastery;
import academy.progress.MasteryCalculator.Coverage;
import academy.progress.MasteryCalculator.Event;

class MasteryCalculatorTest {

    private static final List<Evidence> REQUIRED = List.of(IMPL, MIST, EXPL);
    private static final Instant DAY_0 = Instant.parse("2026-11-01T10:00:00Z");

    private final List<Event> events = new ArrayList<>();

    @Test
    void notStartedUntilTheLessonIsVisited() {
        assertThat(compute(false).level()).isEqualTo(MasteryLevel.NOT_STARTED);
        assertThat(compute(true).level()).isEqualTo(MasteryLevel.INTRODUCED);
    }

    @Test
    void anyPassMeansPractising() {
        practise(0, "write-a", Set.of(IMPL), true, false);

        assertThat(compute(true).level()).isEqualTo(MasteryLevel.PRACTISING);
    }

    @Test
    void assistedPassesNeverReachDemonstrated() {
        practise(0, "write-a", Set.of(IMPL), true, false);
        practise(0, "predict-a", Set.of(MIST), true, false);
        practise(0, "explain-a", Set.of(EXPL), true, false);

        ConceptMastery m = compute(true);

        assertThat(m.level()).isEqualTo(MasteryLevel.PRACTISING);
        assertThat(m.assistedOnlyExercises()).isEqualTo(3);
        assertThat(m.evidence()).containsEntry(IMPL, Coverage.ASSISTED);
    }

    @Test
    void demonstratedNeedsEveryRequiredEvidenceTypeIndependently() {
        practise(0, "write-a", Set.of(IMPL), true, true);
        practise(0, "predict-a", Set.of(MIST), true, true);
        assertThat(compute(true).level()).isEqualTo(MasteryLevel.PRACTISING);
        assertThat(compute(true).evidence()).containsEntry(EXPL, Coverage.MISSING);

        practise(1, "explain-a", Set.of(EXPL), true, true);
        ConceptMastery m = compute(true);

        assertThat(m.level()).isEqualTo(MasteryLevel.DEMONSTRATED);
        assertThat(m.demonstratedAt()).isEqualTo(DAY_0.plus(Duration.ofDays(1)));
        assertThat(m.nextCheckDue()).isEqualTo(DAY_0.plus(Duration.ofDays(4)));
    }

    @Test
    void demonstratedNeedsTwoDistinctExercises() {
        events.add(new Event(DAY_0, "everything", Set.of(IMPL, MIST, EXPL), true, true, false, false));

        assertThat(compute(true).level()).isEqualTo(MasteryLevel.PRACTISING);
    }

    @Test
    void explanationsAwaitingReviewAreShownButDontCount() {
        practise(0, "write-a", Set.of(IMPL), true, true);
        practise(0, "predict-a", Set.of(MIST), true, true);
        events.add(new Event(DAY_0, "explain-a", Set.of(EXPL), false, true, false, true));

        ConceptMastery m = compute(true);

        assertThat(m.level()).isEqualTo(MasteryLevel.PRACTISING);
        assertThat(m.evidence()).containsEntry(EXPL, Coverage.PENDING_REVIEW);
    }

    @Test
    void passingSpacedChecksMakesItSecureThenRetained() {
        demonstrateOnDay(0);

        check(3, true);
        assertThat(compute(true).level()).isEqualTo(MasteryLevel.SECURE);
        assertThat(compute(true).nextCheckDue()).isEqualTo(DAY_0.plus(Duration.ofDays(13)));

        check(13, true);
        assertThat(compute(true).level()).isEqualTo(MasteryLevel.SECURE);
        assertThat(compute(true).nextCheckDue()).isEqualTo(DAY_0.plus(Duration.ofDays(43)));

        check(43, true);
        assertThat(compute(true).level()).isEqualTo(MasteryLevel.RETAINED);
    }

    @Test
    void aFailedCheckDropsOneLevelAndRestartsTheSchedule() {
        demonstrateOnDay(0);
        check(3, true);
        check(13, true);
        check(43, true);

        check(73, false);
        ConceptMastery afterFailure = compute(true);
        assertThat(afterFailure.level()).isEqualTo(MasteryLevel.SECURE);
        assertThat(afterFailure.nextCheckDue()).isEqualTo(DAY_0.plus(Duration.ofDays(76)));

        check(76, false);
        check(79, false);
        assertThat(compute(true).level()).as("never below Demonstrated").isEqualTo(MasteryLevel.DEMONSTRATED);
    }

    @Test
    void anAssistedCheckCountsAsAFailedCheck() {
        demonstrateOnDay(0);
        events.add(new Event(DAY_0.plus(Duration.ofDays(3)), "variant", Set.of(IMPL), true, false, true, false));

        assertThat(compute(true).level()).isEqualTo(MasteryLevel.DEMONSTRATED);
        assertThat(compute(true).nextCheckDue()).isEqualTo(DAY_0.plus(Duration.ofDays(6)));
    }

    @Test
    void reportsWhenACheckIsDue() {
        demonstrateOnDay(0);
        ConceptMastery m = compute(true);

        assertThat(m.checkDue(DAY_0.plus(Duration.ofDays(2)))).isFalse();
        assertThat(m.checkDue(DAY_0.plus(Duration.ofDays(3)))).isTrue();
    }

    @Test
    void onlyRequiredEvidenceIsReported() {
        practise(0, "debug-a", Set.of(DEBUG), true, true);

        assertThat(compute(true).evidence()).containsOnlyKeys(IMPL, MIST, EXPL);
    }

    private void demonstrateOnDay(int day) {
        practise(day, "write-a", Set.of(IMPL), true, true);
        practise(day, "predict-a", Set.of(MIST), true, true);
        practise(day, "explain-a", Set.of(EXPL), true, true);
    }

    private void practise(int day, String exercise, Set<Evidence> evidence, boolean passed, boolean independent) {
        events.add(new Event(DAY_0.plus(Duration.ofDays(day)), exercise, evidence, passed, independent, false, false));
    }

    private void check(int day, boolean passed) {
        events.add(new Event(DAY_0.plus(Duration.ofDays(day)), "variant-" + day, Set.of(IMPL), passed, true, true, false));
    }

    private ConceptMastery compute(boolean introduced) {
        return MasteryCalculator.compute(REQUIRED, events, introduced);
    }
}
