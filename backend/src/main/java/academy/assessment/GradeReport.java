package academy.assessment;

import java.util.List;

import academy.execution.Diagnostic;

/**
 * The result of grading one submission. {@code actualOutput} is the program's real output for
 * predict exercises, revealed after the learner commits to a prediction.
 */
public record GradeReport(
        Outcome outcome,
        String message,
        List<Diagnostic> diagnostics,
        List<TestResult> tests,
        String actualOutput) {

    public enum Outcome { PASSED, FAILED, COMPILE_ERROR, PENDING_REVIEW }

    public boolean passed() {
        return outcome == Outcome.PASSED;
    }

    /** The report with hidden-test details removed. */
    public GradeReport forLearner() {
        return new GradeReport(outcome, message, diagnostics, tests.stream().map(TestResult::redacted).toList(), actualOutput);
    }

    static GradeReport compileError(List<Diagnostic> diagnostics) {
        return new GradeReport(Outcome.COMPILE_ERROR, "Your code doesn't compile yet. Start with the first error.",
                diagnostics, List.of(), null);
    }
}
