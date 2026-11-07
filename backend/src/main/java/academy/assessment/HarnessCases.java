package academy.assessment;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import academy.content.Exercise;
import academy.content.Exercise.MethodSpec;
import academy.content.Exercise.TestCase;

/** Generates the {@code AcademyGraderCases} source that feeds method tests to the grading harness. */
final class HarnessCases {

    static final String CLASS_NAME = "AcademyGraderCases";

    private HarnessCases() {}

    /**
     * @throws IllegalArgumentException if a test case doesn't fit the exercise's declared methods
     */
    static String source(Exercise exercise, List<TestCase> tests, String marker, long caseTimeoutMs) {
        List<MethodSpec> methods = exercise.entry().methodsOrEmpty();
        if (methods.isEmpty()) {
            throw new IllegalArgumentException("Method tests need entry.methods to be declared");
        }
        List<String> caseMethods = new ArrayList<>();
        List<String> caseArgs = new ArrayList<>();
        List<String> caseExpected = new ArrayList<>();
        for (int i = 0; i < tests.size(); i++) {
            TestCase test = tests.get(i);
            String methodName = test.method() == null ? methods.getFirst().name() : test.method();
            int index = indexOf(methods, methodName);
            if (index < 0) {
                throw new IllegalArgumentException("Test " + describe(test, i) + " calls undeclared method " + methodName);
            }
            MethodSpec method = methods.get(index);
            if (test.args().size() != method.params().size()) {
                throw new IllegalArgumentException("Test " + describe(test, i) + " passes " + test.args().size()
                        + " arguments to " + method.signature());
            }
            try {
                List<String> args = new ArrayList<>();
                for (int p = 0; p < test.args().size(); p++) {
                    args.add(JavaLiterals.literal(test.args().get(p), method.params().get(p).type()));
                }
                caseMethods.add(Integer.toString(index));
                caseArgs.add("{" + String.join(", ", args) + "}");
                caseExpected.add(JavaLiterals.literal(test.expect(), method.returns()));
            } catch (IllegalArgumentException | ArithmeticException e) {
                throw new IllegalArgumentException("Test " + describe(test, i) + ": " + e.getMessage(), e);
            }
        }
        double tolerance = exercise.spec().tests().toleranceOrDefault();

        return """
                final class %s {
                    static final String TARGET_CLASS = %s;
                    static final String MARKER = %s;
                    static final long CASE_TIMEOUT_MS = %dL;
                    static final double TOLERANCE = %s;
                    static final String[] METHOD_NAMES = {%s};
                    static final String[] SIGNATURES = {%s};
                    static final Class<?>[][] PARAM_TYPES = {%s};
                    static final Class<?>[] RETURN_TYPES = {%s};
                    static final int[] CASE_METHOD = {%s};

                    static Object[][] caseArgs() {
                        return new Object[][] {%s};
                    }

                    static Object[] caseExpected() {
                        return new Object[] {%s};
                    }
                }
                """.formatted(
                CLASS_NAME,
                JavaLiterals.literal(exercise.entry().mainClass(), "String"),
                JavaLiterals.literal(marker, "String"),
                caseTimeoutMs,
                Double.toString(tolerance),
                methods.stream().map(m -> JavaLiterals.literal(m.name(), "String")).collect(Collectors.joining(", ")),
                methods.stream().map(m -> JavaLiterals.literal(m.signature(), "String")).collect(Collectors.joining(", ")),
                methods.stream().map(m -> "{" + m.params().stream().map(p -> JavaLiterals.classLiteral(p.type()))
                        .collect(Collectors.joining(", ")) + "}").collect(Collectors.joining(", ")),
                methods.stream().map(m -> JavaLiterals.classLiteral(m.returns())).collect(Collectors.joining(", ")),
                String.join(", ", caseMethods),
                String.join(",\n            ", caseArgs),
                String.join(",\n            ", caseExpected));
    }

    private static int indexOf(List<MethodSpec> methods, String name) {
        for (int i = 0; i < methods.size(); i++) {
            if (methods.get(i).name().equals(name)) {
                return i;
            }
        }
        return -1;
    }

    private static String describe(TestCase test, int index) {
        return test.name() == null ? "#" + (index + 1) : "'" + test.name() + "'";
    }
}
