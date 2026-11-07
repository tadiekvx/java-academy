package academy.mentor;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;

import academy.mentor.MentorPolicy.AttemptFact;
import academy.mentor.MentorPolicy.ExerciseHistory;
import academy.mentor.MentorPolicy.Gate;
import academy.mentor.MentorPolicy.MentorEvent;
import academy.mentor.MentorPolicy.Pass;

class MentorPolicyTest {

    private static final Instant T0 = Instant.parse("2026-11-05T10:00:00Z");

    @Test
    void nudgesAreAlwaysAvailable() {
        assertThat(gate(MentorLevel.NUDGE, history(List.of(), null, null), T0).allowed()).isTrue();
    }

    @Test
    void aTargetedHintNeedsOneAttempt() {
        assertThat(gate(MentorLevel.TARGETED_HINT, history(List.of(), null, null), T0).reason()).contains("at least once");
        assertThat(gate(MentorLevel.TARGETED_HINT, history(List.of(attempt(1, "a")), null, null), T0).allowed()).isTrue();
    }

    @Test
    void aWorkedExampleNeedsTwoChangedAttemptsOrTenMinutesAfterTheHint() {
        Instant hint = T0.plus(Duration.ofMinutes(1));
        var sameCodeTwice = history(List.of(attempt(0, "a"), attempt(2, "b"), attempt(3, "b")), hint, null);
        var twoVersions = history(List.of(attempt(0, "a"), attempt(2, "b"), attempt(3, "c")), hint, null);

        assertThat(gate(MentorLevel.WORKED_EXAMPLE, sameCodeTwice, T0.plus(Duration.ofMinutes(4))).allowed()).isFalse();
        assertThat(gate(MentorLevel.WORKED_EXAMPLE, twoVersions, T0.plus(Duration.ofMinutes(4))).allowed()).isTrue();
        assertThat(gate(MentorLevel.WORKED_EXAMPLE, sameCodeTwice, T0.plus(Duration.ofMinutes(11))).allowed()).isTrue();
    }

    @Test
    void aWalkthroughNeedsAnAttemptAfterTheExampleAndConfirmation() {
        Instant hint = T0.plus(Duration.ofMinutes(1));
        Instant example = T0.plus(Duration.ofMinutes(5));
        var noAttemptSince = history(List.of(attempt(0, "a")), hint, example);
        var attemptedSince = history(List.of(attempt(0, "a"), attempt(6, "b")), hint, example);

        assertThat(gate(MentorLevel.WALKTHROUGH, noAttemptSince, T0.plus(Duration.ofMinutes(7))).reason()).contains("Try once more");
        Gate unconfirmed = gate(MentorLevel.WALKTHROUGH, attemptedSince, T0.plus(Duration.ofMinutes(7)));
        assertThat(unconfirmed.needsConfirmation()).isTrue();
        assertThat(unconfirmed.reason()).contains("won't count towards independent mastery");
        assertThat(MentorPolicy.gate(MentorLevel.WALKTHROUGH, MentorLevel.WALKTHROUGH, attemptedSince, false, null, true,
                T0.plus(Duration.ofMinutes(7))).allowed()).isTrue();
    }

    @Test
    void knowledgeChecksAreCappedAtANudge() {
        Gate gate = MentorPolicy.gate(MentorLevel.TARGETED_HINT, MentorLevel.NUDGE, history(List.of(attempt(0, "a")), null, null),
                false, null, false, T0);

        assertThat(gate.allowed()).isFalse();
        assertThat(gate.reason()).contains("knowledge check");
    }

    @Test
    void attemptFirstModeAsksForAHypothesisBeforeATargetedHint() {
        var history = history(List.of(attempt(0, "a")), null, null);

        assertThat(MentorPolicy.gate(MentorLevel.TARGETED_HINT, MentorLevel.WALKTHROUGH, history, true, " ", false, T0).reason())
                .contains("what you think is going wrong");
        assertThat(MentorPolicy.gate(MentorLevel.TARGETED_HINT, MentorLevel.WALKTHROUGH, history, true, "I divide too early", false, T0)
                .allowed()).isTrue();
    }

    @Test
    void threeRecentSolutionRequestsTurnOnAttemptFirstMode() {
        List<MentorEvent> events = new ArrayList<>();
        events.add(learner(1, "e1", true));
        events.add(learner(2, "e1", false));
        events.add(learner(3, "e2", true));
        assertThat(MentorPolicy.attemptFirst(events, List.of())).isFalse();

        events.add(learner(4, "e3", true));
        assertThat(MentorPolicy.attemptFirst(events, List.of())).isTrue();
    }

    @Test
    void workedExamplesOnThreeRecentExercisesTurnOnAttemptFirstMode() {
        List<MentorEvent> events = List.of(mentor(1, "e1", 3), mentor(2, "e2", 4), mentor(3, "e3", 3));

        assertThat(MentorPolicy.attemptFirst(events, List.of())).isTrue();
        assertThat(MentorPolicy.attemptFirst(events.subList(0, 2), List.of())).isFalse();
    }

    @Test
    void attemptFirstModeEndsAfterThreeDifferentExercisesPassedIndependently() {
        List<MentorEvent> events = List.of(learner(1, "e1", true), learner(2, "e1", true), learner(3, "e1", true));
        List<Pass> twoDifferent = List.of(pass(5, "a", true), pass(6, "a", true), pass(7, "b", true), pass(8, "c", false));
        List<Pass> threeDifferent = List.of(pass(5, "a", true), pass(7, "b", true), pass(9, "c", true));
        List<Pass> beforeTrigger = List.of(pass(0, "a", true), pass(0, "b", true), pass(0, "c", true));

        assertThat(MentorPolicy.attemptFirst(events, twoDifferent)).isTrue();
        assertThat(MentorPolicy.attemptFirst(events, threeDifferent)).isFalse();
        assertThat(MentorPolicy.attemptFirst(events, beforeTrigger)).isTrue();
    }

    private static Gate gate(MentorLevel target, ExerciseHistory history, Instant now) {
        return MentorPolicy.gate(target, MentorLevel.WALKTHROUGH, history, false, null, false, now);
    }

    private static ExerciseHistory history(List<AttemptFact> attempts, Instant hint, Instant example) {
        return new ExerciseHistory(attempts, hint, example);
    }

    private static AttemptFact attempt(int minute, String hash) {
        return new AttemptFact(T0.plus(Duration.ofMinutes(minute)), hash);
    }

    private static MentorEvent learner(int minute, String exercise, boolean solutionRequest) {
        return new MentorEvent(T0.plus(Duration.ofMinutes(minute)), exercise, true, solutionRequest, 1);
    }

    private static MentorEvent mentor(int minute, String exercise, int level) {
        return new MentorEvent(T0.plus(Duration.ofMinutes(minute)), exercise, false, false, level);
    }

    private static Pass pass(int minute, String exercise, boolean independent) {
        return new Pass(T0.plus(Duration.ofMinutes(minute)), exercise, independent);
    }
}
