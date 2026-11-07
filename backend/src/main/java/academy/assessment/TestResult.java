package academy.assessment;

/**
 * The result of one test. {@code call} describes the input (e.g. {@code average(3, 4)} or the
 * stdin given); {@code output} is anything the code printed while the test ran.
 */
public record TestResult(
        String name,
        boolean visible,
        Status status,
        String call,
        String expected,
        String actual,
        String output,
        String error) {

    public enum Status { PASS, FAIL, ERROR, TIMEOUT, NOT_RUN }

    public boolean passed() {
        return status == Status.PASS;
    }

    /** What a learner may see of a hidden test: its name and whether it passed. */
    TestResult redacted() {
        return visible ? this : new TestResult(name, false, status, null, null, null, null, null);
    }
}
