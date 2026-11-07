import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.lang.reflect.Array;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

/**
 * Grading harness, compiled together with the learner's code and a generated
 * {@code AcademyGraderCases} class. It calls the learner's methods reflectively (the class
 * declared implicitly by a compact source file can't be named in source) and prints one
 * marker-prefixed JSON line per test case on the real standard output.
 *
 * <p>This file is a resource of the platform, not part of the platform's own code.
 */
final class AcademyGrader {

    private static final int MAX_CAPTURED_OUTPUT = 2000;
    private static final int MAX_REPORTED_FRAMES = 12;

    public static void main(String[] args) throws Exception {
        PrintStream report = System.out;
        Object[][] caseArgs = AcademyGraderCases.caseArgs();
        Object[] caseExpected = AcademyGraderCases.caseExpected();

        Class<?> target;
        try {
            target = Class.forName(AcademyGraderCases.TARGET_CLASS);
        } catch (ClassNotFoundException e) {
            for (int i = 0; i < caseArgs.length; i++) {
                emit(report, i, "error", null, null, "", "Could not find the class " + AcademyGraderCases.TARGET_CLASS + ".");
            }
            return;
        }

        Method[] methods = new Method[AcademyGraderCases.METHOD_NAMES.length];
        String[] problems = new String[methods.length];
        for (int m = 0; m < methods.length; m++) {
            try {
                methods[m] = resolve(target, m);
            } catch (IllegalStateException e) {
                problems[m] = e.getMessage();
            }
        }

        for (int i = 0; i < caseArgs.length; i++) {
            int m = AcademyGraderCases.CASE_METHOD[i];
            String expectedText = show(caseExpected[i]);
            if (methods[m] == null) {
                emit(report, i, "error", expectedText, null, "", problems[m]);
                continue;
            }
            Method method = methods[m];
            Object[] callArgs = caseArgs[i];

            ByteArrayOutputStream captured = new ByteArrayOutputStream();
            PrintStream capture = new PrintStream(captured, true, StandardCharsets.UTF_8);
            System.setOut(capture);
            System.setErr(capture);
            FutureTask<Object> task = new FutureTask<>(() -> {
                Object instance = Modifier.isStatic(method.getModifiers()) ? null : newInstance(target);
                return method.invoke(instance, callArgs);
            });
            Thread thread = new Thread(task, "learner-code");
            thread.setDaemon(true);
            thread.start();

            String status;
            String actualText = null;
            String error = null;
            boolean timedOut = false;
            try {
                Object actual = task.get(AcademyGraderCases.CASE_TIMEOUT_MS, TimeUnit.MILLISECONDS);
                actualText = show(actual);
                status = matches(caseExpected[i], actual) ? "pass" : "fail";
            } catch (TimeoutException e) {
                status = "timeout";
                error = "Took longer than " + AcademyGraderCases.CASE_TIMEOUT_MS + " ms. Is there a loop that never ends?";
                timedOut = true;
            } catch (ExecutionException e) {
                status = "error";
                Throwable cause = e.getCause() instanceof InvocationTargetException ite ? ite.getCause() : e.getCause();
                error = describe(cause, target);
            } finally {
                System.setOut(report);
                System.setErr(report);
            }
            emit(report, i, status, expectedText, actualText, truncate(captured.toString(StandardCharsets.UTF_8)), error);
            if (timedOut) {
                // A runaway thread can't be stopped safely; end the run. Remaining cases are reported as not run.
                report.flush();
                Runtime.getRuntime().halt(0);
            }
        }
        report.flush();
    }

    private static Method resolve(Class<?> target, int m) {
        String name = AcademyGraderCases.METHOD_NAMES[m];
        Class<?>[] wanted = AcademyGraderCases.PARAM_TYPES[m];
        String signature = AcademyGraderCases.SIGNATURES[m];
        List<Method> candidates = new ArrayList<>();
        for (Method method : target.getDeclaredMethods()) {
            if (method.getName().equals(name)) {
                candidates.add(method);
            }
        }
        if (candidates.isEmpty()) {
            throw new IllegalStateException("Couldn't find a method called `" + name + "`. The tests expect `" + signature + "`.");
        }
        for (Method method : candidates) {
            Class<?>[] actual = method.getParameterTypes();
            if (actual.length != wanted.length) {
                continue;
            }
            boolean ok = compatible(AcademyGraderCases.RETURN_TYPES[m], method.getReturnType());
            for (int p = 0; p < actual.length && ok; p++) {
                ok = compatible(wanted[p], actual[p]);
            }
            if (ok) {
                method.setAccessible(true);
                return method;
            }
        }
        throw new IllegalStateException("The tests expect `" + signature + "`, but your method is `"
                + describe(candidates.get(0)) + "`. Check the return type and the parameter types.");
    }

    private static boolean compatible(Class<?> wanted, Class<?> actual) {
        return wanted == actual || (List.class.isAssignableFrom(wanted) && List.class.isAssignableFrom(actual));
    }

    private static Object newInstance(Class<?> target) throws Exception {
        Constructor<?> constructor = target.getDeclaredConstructor();
        constructor.setAccessible(true);
        return constructor.newInstance();
    }

    private static boolean matches(Object expected, Object actual) {
        if (expected instanceof Double || expected instanceof Float) {
            return actual instanceof Number n && closeEnough(((Number) expected).doubleValue(), n.doubleValue());
        }
        if (expected instanceof double[] e && actual instanceof double[] a) {
            if (e.length != a.length) {
                return false;
            }
            for (int i = 0; i < e.length; i++) {
                if (!closeEnough(e[i], a[i])) {
                    return false;
                }
            }
            return true;
        }
        if (expected instanceof List<?> e && actual instanceof List<?> a) {
            if (e.size() != a.size()) {
                return false;
            }
            for (int i = 0; i < e.size(); i++) {
                if (!matches(e.get(i), a.get(i))) {
                    return false;
                }
            }
            return true;
        }
        if (expected != null && expected.getClass().isArray()) {
            return Arrays.deepEquals(new Object[] {expected}, new Object[] {actual});
        }
        return Objects.equals(expected, actual);
    }

    private static boolean closeEnough(double expected, double actual) {
        if (Double.isNaN(expected) || Double.isInfinite(expected)) {
            return Double.compare(expected, actual) == 0;
        }
        return Math.abs(expected - actual) <= AcademyGraderCases.TOLERANCE;
    }

    /** Formats a value the way it would be written in Java, so learners can compare like with like. */
    private static String show(Object value) {
        if (value == null) {
            return "null";
        }
        if (value instanceof String s) {
            return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\t", "\\t") + "\"";
        }
        if (value instanceof Character c) {
            return "'" + c + "'";
        }
        if (value instanceof Collection<?> collection) {
            List<String> parts = new ArrayList<>();
            for (Object element : collection) {
                parts.add(show(element));
            }
            return "[" + String.join(", ", parts) + "]";
        }
        if (value.getClass().isArray()) {
            List<String> parts = new ArrayList<>();
            for (int i = 0; i < Array.getLength(value); i++) {
                parts.add(show(Array.get(value, i)));
            }
            return "[" + String.join(", ", parts) + "]";
        }
        return String.valueOf(value);
    }

    private static String describe(Method method) {
        List<String> params = new ArrayList<>();
        for (Class<?> type : method.getParameterTypes()) {
            params.add(type.getSimpleName());
        }
        return method.getReturnType().getSimpleName() + " " + method.getName() + "(" + String.join(", ", params) + ")";
    }

    /** Describes an exception with the stack frames that belong to the learner's own code. */
    private static String describe(Throwable t, Class<?> target) {
        StringBuilder text = new StringBuilder(t.getClass().getName());
        if (t.getMessage() != null) {
            text.append(": ").append(t.getMessage());
        }
        int shown = 0;
        int omitted = 0;
        for (StackTraceElement frame : t.getStackTrace()) {
            String owner = frame.getClassName();
            if (owner.equals(target.getName()) || owner.startsWith(target.getName() + "$")) {
                if (shown < MAX_REPORTED_FRAMES) {
                    text.append("\n    at ").append(frame.getMethodName())
                            .append("(").append(frame.getFileName()).append(":").append(frame.getLineNumber()).append(")");
                    shown++;
                } else {
                    omitted++;
                }
            }
        }
        if (omitted > 0) {
            // A runaway recursion has thousands of frames; one report line must stay small enough to arrive intact.
            text.append("\n    ... and ").append(omitted).append(" more frames");
        }
        return text.toString();
    }

    private static String truncate(String text) {
        return text.length() <= MAX_CAPTURED_OUTPUT ? text : text.substring(0, MAX_CAPTURED_OUTPUT) + "\n[output truncated]";
    }

    private static void emit(PrintStream out, int index, String status, String expected, String actual, String output, String error) {
        out.println(AcademyGraderCases.MARKER + "{\"index\":" + index
                + ",\"status\":" + json(status)
                + ",\"expected\":" + json(expected)
                + ",\"actual\":" + json(actual)
                + ",\"output\":" + json(output)
                + ",\"error\":" + json(error) + "}");
    }

    private static String json(String s) {
        if (s == null) {
            return "null";
        }
        StringBuilder b = new StringBuilder("\"");
        for (char c : s.toCharArray()) {
            switch (c) {
                case '"' -> b.append("\\\"");
                case '\\' -> b.append("\\\\");
                case '\n' -> b.append("\\n");
                case '\r' -> b.append("\\r");
                case '\t' -> b.append("\\t");
                default -> {
                    if (c < 0x20) {
                        b.append(String.format("\\u%04x", (int) c));
                    } else {
                        b.append(c);
                    }
                }
            }
        }
        return b.append('"').toString();
    }
}
