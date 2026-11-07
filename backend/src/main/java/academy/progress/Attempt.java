package academy.progress;

import java.time.Instant;

import academy.assessment.GradeReport;

/** One recorded attempt. Attempts are never changed after they are written. */
public record Attempt(
        long id,
        long learnerId,
        String exerciseId,
        Instant submittedAt,
        AttemptContext context,
        GradeReport.Outcome outcome,
        int testsPassed,
        int testsTotal,
        int assistanceLevel,
        boolean solutionViewed,
        String submissionHash) {

    public boolean passed() {
        return outcome == GradeReport.Outcome.PASSED;
    }
}
