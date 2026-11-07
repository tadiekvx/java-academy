package academy.assessment;

import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import academy.content.Exercise;
import academy.content.Exercise.TestCase;
import academy.content.Exercise.VisibleTest;
import academy.execution.CompileResult;
import academy.execution.CompiledProgram;
import academy.execution.Diagnostic;
import academy.execution.ExecutionLimits;
import academy.execution.LocalJvmRunner;
import academy.execution.RunResult;
import academy.execution.SourceFile;
import tools.jackson.databind.json.JsonMapper;

/** Grades submissions by compiling and running them against the exercise's tests. */
@Service
public class Grader {

    private static final String HARNESS_FILE = "AcademyGrader.java";
    private static final long DEFAULT_CASE_TIMEOUT_MS = 2000;
    private static final int MAX_SHOWN_ERROR_OUTPUT = 2000;

    private final LocalJvmRunner runner;
    private final String harnessSource = loadHarness();
    private final JsonMapper json = JsonMapper.builder().build();

    public Grader(LocalJvmRunner runner) {
        this.runner = runner;
    }

    public GradeReport grade(Exercise exercise, Submission submission) {
        return switch (exercise.type()) {
            case WRITE, DEBUG, MODIFY -> gradeCode(exercise, submission.files() == null ? Map.of() : submission.files());
            case PARSONS -> gradeParsons(exercise, submission.order());
            case PREDICT -> gradePrediction(exercise, submission.prediction());
            case EXPLAIN -> new GradeReport(GradeReport.Outcome.PENDING_REVIEW,
                    "Thanks. Your explanation has been saved for review against the rubric.", List.of(), List.of(), null);
        };
    }

    /** Compiles and runs a program as-is, e.g. for a lesson snippet or the editor's Run button. */
    public ProgramRun runProgram(Map<String, String> files, String mainClass, String stdin) {
        CompileResult compiled = runner.compile(toSources(files));
        if (!compiled.succeeded()) {
            return new ProgramRun(compiled.diagnostics(), null);
        }
        try (CompiledProgram program = compiled.program()) {
            return new ProgramRun(compiled.diagnostics(), runner.run(program, mainClass, stdin, ExecutionLimits.DEFAULT));
        }
    }

    public record ProgramRun(List<Diagnostic> diagnostics, RunResult result) {

        public boolean compiled() {
            return result != null;
        }
    }

    /** Grades the given source files against the exercise's tests, whatever the exercise type. */
    public GradeReport gradeFiles(Exercise exercise, Map<String, String> files) {
        return gradeCode(exercise, files);
    }

    GradeReport gradeCode(Exercise exercise, Map<String, String> files) {
        if (files.keySet().stream().anyMatch(name -> name.startsWith("AcademyGrader"))) {
            throw new IllegalArgumentException("File names starting with AcademyGrader are reserved");
        }
        List<VisibleTest> methodTests = exercise.allTests().filter(t -> t.test().isMethodTest()).toList();
        List<VisibleTest> ioTests = exercise.allTests().filter(t -> t.test().isIoTest()).toList();
        List<VisibleTest> sourceTests = exercise.allTests().filter(t -> t.test().isSourceTest()).toList();
        long caseTimeoutMs = exercise.spec().limits() != null && exercise.spec().limits().timeMs() != null
                ? exercise.spec().limits().timeMs() : DEFAULT_CASE_TIMEOUT_MS;
        String marker = "@@academy-" + UUID.randomUUID() + "@@";

        List<SourceFile> sources = toSources(files);
        if (!methodTests.isEmpty()) {
            sources.add(new SourceFile(HARNESS_FILE, harnessSource));
            sources.add(new SourceFile(HarnessCases.CLASS_NAME + ".java", HarnessCases.source(
                    exercise, methodTests.stream().map(VisibleTest::test).toList(), marker, caseTimeoutMs)));
        }

        CompileResult compiled = runner.compile(sources);
        Set<String> learnerFiles = files.keySet();
        List<Diagnostic> learnerDiagnostics = compiled.diagnostics().stream()
                .filter(d -> d.file() == null || learnerFiles.contains(d.file()))
                .toList();
        if (!compiled.succeeded()) {
            if (learnerDiagnostics.stream().noneMatch(d -> d.kind() == Diagnostic.Kind.ERROR)) {
                throw new IllegalStateException("Grading harness failed to compile: " + compiled.diagnostics());
            }
            return GradeReport.compileError(learnerDiagnostics);
        }

        List<TestResult> results = new ArrayList<>();
        try (CompiledProgram program = compiled.program()) {
            if (!methodTests.isEmpty()) {
                results.addAll(runMethodTests(program, methodTests, marker, caseTimeoutMs, exercise));
            }
            for (VisibleTest test : ioTests) {
                results.add(runIoTest(program, exercise, test));
            }
        }
        for (VisibleTest test : sourceTests) {
            results.add(checkSource(exercise, test, files));
        }
        long failures = results.stream().filter(r -> !r.passed()).count();
        String message;
        if (failures == 0) {
            message = results.size() == 1 ? "The test passed." : "All " + results.size() + " tests passed.";
        } else {
            message = results.size() == 1 ? "The test didn't pass yet." : failures + " of " + results.size() + " tests didn't pass yet.";
        }
        return new GradeReport(failures == 0 ? GradeReport.Outcome.PASSED : GradeReport.Outcome.FAILED,
                message, learnerDiagnostics, results, null);
    }

    private List<TestResult> runMethodTests(CompiledProgram program, List<VisibleTest> tests, String marker,
            long caseTimeoutMs, Exercise exercise) {
        var limits = ExecutionLimits.DEFAULT.withTimeout(Duration.ofMillis(tests.size() * caseTimeoutMs + 5000));
        RunResult run = runner.run(program, "AcademyGrader", "", limits);

        HarnessLine[] lines = new HarnessLine[tests.size()];
        run.stdout().lines()
                .filter(line -> line.startsWith(marker))
                .map(line -> json.readValue(line.substring(marker.length()), HarnessLine.class))
                .filter(line -> line.index() >= 0 && line.index() < lines.length)
                .forEach(line -> lines[line.index()] = line);

        List<TestResult> results = new ArrayList<>();
        for (int i = 0; i < tests.size(); i++) {
            VisibleTest vt = tests.get(i);
            TestCase test = vt.test();
            String call = TestDescriptions.call(exercise, test);
            HarnessLine line = lines[i];
            if (line == null) {
                String reason = run.stderr().isBlank()
                        ? "Not run: the program stopped early (an earlier test timed out, or the code called System.exit)."
                        : "Not run: the program stopped early.\n" + truncate(run.stderr());
                results.add(new TestResult(test.name(), vt.visible(), TestResult.Status.NOT_RUN, call, TestDescriptions.expected(test),
                        null, null, reason));
                continue;
            }
            results.add(new TestResult(test.name(), vt.visible(), status(line.status()), call, line.expected(),
                    line.actual(), line.output(), line.error()));
        }
        return results;
    }

    /** Checks required and forbidden text in the learner's source, with whitespace collapsed to single spaces. */
    private TestResult checkSource(Exercise exercise, VisibleTest vt, Map<String, String> files) {
        TestCase test = vt.test();
        String source = files.values().stream().map(Grader::collapseWhitespace).collect(Collectors.joining(" "));
        List<String> problems = new ArrayList<>();
        if (test.sourceContains() != null) {
            test.sourceContains().stream().filter(s -> !source.contains(collapseWhitespace(s)))
                    .forEach(s -> problems.add("missing " + TestDescriptions.show(s)));
        }
        if (test.sourceNotContains() != null) {
            test.sourceNotContains().stream().filter(s -> source.contains(collapseWhitespace(s)))
                    .forEach(s -> problems.add("found " + TestDescriptions.show(s) + ", which this exercise doesn't allow"));
        }
        boolean ok = problems.isEmpty();
        return new TestResult(test.name(), vt.visible(), ok ? TestResult.Status.PASS : TestResult.Status.FAIL,
                TestDescriptions.call(exercise, test), TestDescriptions.expected(test), ok ? null : String.join("; ", problems), null, null);
    }

    private static String collapseWhitespace(String text) {
        return text.replaceAll("\\s+", " ").strip();
    }

    private TestResult runIoTest(CompiledProgram program, Exercise exercise, VisibleTest vt) {
        TestCase test = vt.test();
        String stdin = test.stdin() == null ? "" : test.stdin();
        String call = TestDescriptions.call(exercise, test);
        String expected = TestDescriptions.expected(test);
        RunResult run = runner.run(program, exercise.entry().mainClass(), stdin, ExecutionLimits.DEFAULT);

        TestResult.Status status;
        String error = null;
        if (run.timedOut()) {
            status = TestResult.Status.TIMEOUT;
            error = "The program didn't finish in time. Is there a loop that never ends, or is it waiting for more input?";
        } else if (run.outputLimitExceeded()) {
            status = TestResult.Status.ERROR;
            error = "The program printed too much output and was stopped.";
        } else if (run.exitCode() != 0) {
            status = TestResult.Status.ERROR;
            error = truncate(run.stderr());
        } else {
            boolean ok = test.stdoutEquals() != null
                    ? normalize(run.stdout()).equals(normalize(test.stdoutEquals()))
                    : test.stdoutContains().stream().allMatch(s -> run.stdout().contains(s));
            status = ok ? TestResult.Status.PASS : TestResult.Status.FAIL;
        }
        return new TestResult(test.name(), vt.visible(), status, call, expected, run.stdout(), null, error);
    }

    private GradeReport gradeParsons(Exercise exercise, List<Integer> order) {
        List<String> palette = exercise.parsonsPalette();
        if (order == null || order.isEmpty()) {
            return new GradeReport(GradeReport.Outcome.FAILED, "Arrange some blocks first.", List.of(), List.of(), null);
        }
        Set<Integer> seen = new HashSet<>();
        for (int index : order) {
            if (index < 0 || index >= palette.size() || !seen.add(index)) {
                throw new IllegalArgumentException("Invalid block order " + order);
            }
        }
        String source = order.stream().map(palette::get).collect(Collectors.joining("\n", "", "\n"));
        return gradeCode(exercise, Map.of(exercise.entry().mainFile(), source));
    }

    private GradeReport gradePrediction(Exercise exercise, String prediction) {
        ProgramRun run = runProgram(exercise.starter(), exercise.entry().mainClass(), "");
        if (!run.compiled() || !run.result().completedNormally()) {
            throw new IllegalStateException("Predict exercise " + exercise.id() + " doesn't run cleanly");
        }
        String actual = run.result().stdout();
        boolean correct = prediction != null && normalize(prediction).equals(normalize(actual));
        return new GradeReport(correct ? GradeReport.Outcome.PASSED : GradeReport.Outcome.FAILED,
                correct ? "Your prediction was exactly right." : "Not quite. Compare your prediction with the real output line by line.",
                List.of(), List.of(), actual);
    }

    /** Ignores trailing spaces on each line and trailing blank lines, which learners can't see. */
    public static String normalize(String output) {
        return output.replace("\r\n", "\n").lines().map(String::stripTrailing)
                .collect(Collectors.joining("\n")).stripTrailing();
    }

    private static TestResult.Status status(String harnessStatus) {
        return switch (harnessStatus) {
            case "pass" -> TestResult.Status.PASS;
            case "fail" -> TestResult.Status.FAIL;
            case "timeout" -> TestResult.Status.TIMEOUT;
            default -> TestResult.Status.ERROR;
        };
    }

    private static String truncate(String text) {
        return text.length() <= MAX_SHOWN_ERROR_OUTPUT ? text : text.substring(0, MAX_SHOWN_ERROR_OUTPUT) + "\n[truncated]";
    }

    private static List<SourceFile> toSources(Map<String, String> files) {
        return files.entrySet().stream().map(e -> new SourceFile(e.getKey(), e.getValue()))
                .collect(Collectors.toCollection(ArrayList::new));
    }

    private static String loadHarness() {
        try (InputStream in = Grader.class.getResourceAsStream("/academy/assessment/" + HARNESS_FILE)) {
            if (in == null) {
                throw new IllegalStateException("Missing grading harness resource " + HARNESS_FILE);
            }
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private record HarnessLine(int index, String status, String expected, String actual, String output, String error) {}
}
