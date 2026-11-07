package academy.assessment;

import java.util.List;
import java.util.stream.Collectors;

import academy.content.Exercise;
import academy.content.Exercise.TestCase;

/** Human-readable descriptions of a test's input and expected result, written as Java-like values. */
public final class TestDescriptions {

    private TestDescriptions() {}

    public static String call(Exercise exercise, TestCase test) {
        if (test.isMethodTest()) {
            String method = test.method() == null ? exercise.entry().methodsOrEmpty().getFirst().name() : test.method();
            return method + "(" + test.args().stream().map(TestDescriptions::show).collect(Collectors.joining(", ")) + ")";
        }
        if (test.isSourceTest()) {
            return "the form of your code";
        }
        String stdin = test.stdin() == null ? "" : test.stdin();
        return stdin.isEmpty() ? "(no input)" : "input: " + show(stdin);
    }

    public static String expected(TestCase test) {
        if (test.isMethodTest()) {
            return show(test.expect());
        }
        if (test.isSourceTest()) {
            return describeSource(test);
        }
        return test.stdoutEquals() != null
                ? test.stdoutEquals()
                : "output containing " + test.stdoutContains().stream().map(TestDescriptions::show).collect(Collectors.joining(", "));
    }

    private static String describeSource(TestCase test) {
        List<String> parts = new java.util.ArrayList<>();
        if (test.sourceContains() != null) {
            test.sourceContains().forEach(s -> parts.add("contains " + show(s)));
        }
        if (test.sourceNotContains() != null) {
            test.sourceNotContains().forEach(s -> parts.add("does not contain " + show(s)));
        }
        return String.join("; ", parts);
    }

    static String show(Object value) {
        if (value instanceof String s) {
            return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n") + "\"";
        }
        if (value instanceof List<?> list) {
            return list.stream().map(TestDescriptions::show).collect(Collectors.joining(", ", "[", "]"));
        }
        return String.valueOf(value);
    }
}
