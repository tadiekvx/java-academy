package academy.assessment;

import static org.assertj.core.api.Assertions.assertThat;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;

import academy.assessment.TestResult.Status;
import academy.content.Evidence;
import academy.content.Exercise;
import academy.content.Exercise.Entry;
import academy.content.Exercise.MethodSpec;
import academy.content.Exercise.Param;
import academy.content.Exercise.TestCase;
import academy.content.Exercise.Tests;
import academy.content.ExerciseType;
import academy.execution.LocalJvmRunner;

class GraderTest {

    private static final Entry AVERAGE = new Entry(null, List.of(new MethodSpec("average",
            List.of(new Param("a", "int"), new Param("b", "int")), "double")));
    private static final Tests AVERAGE_TESTS = new Tests(
            List.of(methodTest(List.of(3, 4), 3.5), methodTest(List.of(10, 10), 10)),
            List.of(methodTest(List.of(1, -2), -0.5)),
            null);

    private final Grader grader = new Grader(new LocalJvmRunner());

    @Test
    void passesACorrectSolution() {
        GradeReport report = grade(AVERAGE, AVERAGE_TESTS, """
                double average(int a, int b) {
                    return (a + b) / 2.0;
                }
                """);

        assertThat(report.outcome()).isEqualTo(GradeReport.Outcome.PASSED);
        assertThat(report.tests()).hasSize(3).allMatch(TestResult::passed);
    }

    @Test
    void showsExpectedAndActualValuesForAFailure() {
        GradeReport report = grade(AVERAGE, AVERAGE_TESTS, """
                double average(int a, int b) {
                    return (a + b) / 2;
                }
                """);

        assertThat(report.outcome()).isEqualTo(GradeReport.Outcome.FAILED);
        assertThat(report.tests().getFirst()).satisfies(t -> {
            assertThat(t.status()).isEqualTo(Status.FAIL);
            assertThat(t.call()).isEqualTo("average(3, 4)");
            assertThat(t.expected()).isEqualTo("3.5");
            assertThat(t.actual()).isEqualTo("3.0");
        });
    }

    @Test
    void redactsHiddenTestsForLearners() {
        GradeReport report = grade(AVERAGE, AVERAGE_TESTS, """
                double average(int a, int b) {
                    return (a + b) / 2;
                }
                """).forLearner();

        TestResult hidden = report.tests().getLast();
        assertThat(hidden.visible()).isFalse();
        assertThat(hidden.status()).isEqualTo(Status.FAIL);
        assertThat(hidden.call()).isNull();
        assertThat(hidden.expected()).isNull();
        assertThat(hidden.actual()).isNull();
    }

    @Test
    void reportsExceptionsWithTheLearnersLineNumber() {
        Entry divide = new Entry(null, List.of(new MethodSpec("divide",
                List.of(new Param("a", "int"), new Param("b", "int")), "int")));
        GradeReport report = grade(divide, new Tests(List.of(methodTest(List.of(1, 0), 0)), List.of(), null), """
                int divide(int a, int b) {
                    return a / b;
                }
                """);

        assertThat(report.tests().getFirst()).satisfies(t -> {
            assertThat(t.status()).isEqualTo(Status.ERROR);
            assertThat(t.error()).startsWith("java.lang.ArithmeticException: / by zero").contains("divide(Main.java:2)");
        });
    }

    @Test
    void stopsAnInfiniteLoopAndMarksLaterTestsAsNotRun() {
        Entry entry = new Entry(null, List.of(new MethodSpec("countDown", List.of(new Param("n", "int")), "int")));
        GradeReport report = grade(entry, new Tests(List.of(methodTest(List.of(3), 0), methodTest(List.of(5), 0)), List.of(), null), """
                int countDown(int n) {
                    while (n > 0) {
                        n = n * 1;
                    }
                    return n;
                }
                """);

        assertThat(report.tests()).extracting(TestResult::status).containsExactly(Status.TIMEOUT, Status.NOT_RUN);
    }

    @Test
    void explainsASignatureMismatch() {
        GradeReport report = grade(AVERAGE, AVERAGE_TESTS, """
                int average(int a, int b) {
                    return (a + b) / 2;
                }
                """);

        assertThat(report.tests().getFirst().error())
                .contains("double average(int a, int b)")
                .contains("int average(int, int)");
    }

    @Test
    void capturesWhatTheMethodPrinted() {
        GradeReport report = grade(AVERAGE, AVERAGE_TESTS, """
                double average(int a, int b) {
                    IO.println("a=" + a);
                    return (a + b) / 2.0;
                }
                """);

        assertThat(report.tests().getFirst().output()).isEqualTo("a=3\n");
    }

    @Test
    void reportsCompileErrorsOnlyForTheLearnersFiles() {
        GradeReport report = grade(AVERAGE, AVERAGE_TESTS, """
                double average(int a, int b) {
                    return (a + b) / 2.0
                }
                """);

        assertThat(report.outcome()).isEqualTo(GradeReport.Outcome.COMPILE_ERROR);
        assertThat(report.diagnostics()).isNotEmpty().allMatch(d -> d.file().equals("Main.java"));
    }

    @Test
    void gradesInputOutputTests() {
        Tests tests = new Tests(List.of(
                new TestCase(null, null, null, null, "4\n", "Double: 8", null, null, null),
                new TestCase(null, null, null, null, "10\n", null, List.of("20"), null, null)), List.of(), null);
        String source = """
                void main() {
                    int n = Integer.parseInt(IO.readln("Number? "));
                    IO.println();
                    IO.println("Double: " + (n * 2));
                }
                """;

        GradeReport report = grade(new Entry(null, null), tests, source);

        assertThat(report.tests()).extracting(TestResult::status).containsExactly(Status.FAIL, Status.PASS);
        assertThat(report.tests().getFirst().actual()).isEqualTo("Number? \nDouble: 8\n");
    }

    @Test
    void gradesPredictionsAgainstTheRealOutput() {
        Exercise predict = exercise(ExerciseType.PREDICT, new Entry(null, null), null, """
                void main() {
                    IO.println(7 / 2);
                }
                """);

        GradeReport wrong = grader.grade(predict, new Submission(null, "3.5", null, null));
        GradeReport right = grader.grade(predict, new Submission(null, "3  \n\n", null, null));

        assertThat(wrong.passed()).isFalse();
        assertThat(wrong.actualOutput()).isEqualTo("3\n");
        assertThat(right.passed()).isTrue();
    }

    /** Grades a compact source file; adds an empty main method when the source has none, as the compiler requires one. */
    @Test
    void checksTheFormOfTheSource() {
        Tests tests = new Tests(List.of(
                new TestCase("classic main", null, null, null, null, null, null, List.of("public class Main", "public static void main(String[] args)"), null),
                new TestCase("no compact main", null, null, null, null, null, null, null, List.of("void main() {"))), List.of(), null);
        String classic = "public class Main {\n    public static void main(String[] args) {\n        System.out.println(\"Hi\");\n    }\n}\n";
        String compact = "void main() {\n    IO.println(\"Hi\");\n}\n";

        GradeReport good = grader.grade(exercise(ExerciseType.WRITE, new Entry(null, null), tests, ""), Submission.ofFiles(Map.of("Main.java", classic)));
        GradeReport bad = grader.grade(exercise(ExerciseType.WRITE, new Entry(null, null), tests, ""), Submission.ofFiles(Map.of("Main.java", compact)));

        assertThat(good.outcome()).isEqualTo(GradeReport.Outcome.PASSED);
        assertThat(bad.outcome()).isEqualTo(GradeReport.Outcome.FAILED);
        assertThat(bad.tests().getFirst().actual()).contains("missing \"public class Main\"");
        assertThat(bad.tests().getLast().actual()).contains("found \"void main() {\"");
    }

    @Test
    void reportsRunawayRecursionCompactly() {
        // A StackOverflowError carries thousands of frames. The report line must stay small enough to arrive intact.
        Entry entry = new Entry(null, List.of(new MethodSpec("sumTo", List.of(new Param("n", "int")), "long")));
        Tests tests = new Tests(List.of(methodTest(List.of(5), 15)), List.of(), null);

        GradeReport report = grade(entry, tests, """
                long sumTo(int n) {
                    return n + sumTo(n - 1);
                }
                """);

        assertThat(report.outcome()).isEqualTo(GradeReport.Outcome.FAILED);
        assertThat(report.tests().getFirst()).satisfies(t -> {
            assertThat(t.status()).isEqualTo(Status.ERROR);
            assertThat(t.error()).startsWith("java.lang.StackOverflowError").contains("more frames");
            assertThat(t.error().length()).isLessThan(1500);
        });
    }

    private GradeReport grade(Entry entry, Tests tests, String source) {
        String file = source.contains("void main()") ? source : source + "\nvoid main() {\n}\n";
        return grader.grade(exercise(ExerciseType.WRITE, entry, tests, ""), Submission.ofFiles(Map.of("Main.java", file)));
    }

    private static TestCase methodTest(List<Object> args, Object expect) {
        return new TestCase(null, null, args, expect, null, null, null, null, null);
    }

    private static Exercise exercise(ExerciseType type, Entry entry, Tests tests, String starter) {
        var spec = new Exercise.Spec("test-exercise", type, "Test", "j1-l0", Exercise.Role.LADDER, List.of("o1"),
                List.of("J1.02"), List.of(Evidence.IMPL), List.of(), 1, null, "Prompt", entry, tests, null,
                null, null, null, null, null, null, null, false);
        return new Exercise(spec, Path.of("test-exercise"), Map.of("Main.java", starter), Map.of(), Map.of());
    }
}
