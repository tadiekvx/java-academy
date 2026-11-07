package academy.content;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * An exercise: the parsed {@code exercise.yaml} plus its code files. File maps go from file name
 * to content; {@code wrong} goes from the known-wrong solution's name to the content of its single
 * replacement source file.
 */
public record Exercise(
        Spec spec,
        Path dir,
        Map<String, String> starter,
        Map<String, String> solution,
        Map<String, String> wrong) {

    public enum Role { LADDER, RETRIEVAL }

    public record Spec(
            String id,
            ExerciseType type,
            String title,
            String lesson,
            Role role,
            List<String> assesses,
            List<String> concepts,
            List<Evidence> evidence,
            List<String> misconceptions,
            Integer difficulty,
            String variantGroup,
            String prompt,
            Entry entry,
            Tests tests,
            String expectedOutput,
            List<String> blocks,
            List<String> distractors,
            Rubric rubric,
            String refersTo,
            Hints hints,
            Boolean starterCompiles,
            Limits limits,
            Boolean aiAssisted) {}

    /** The class the learner works in and the methods the tests call. */
    public record Entry(@JsonProperty("class") String className, List<MethodSpec> methods) {

        public String mainClass() {
            return className == null ? "Main" : className;
        }

        public String mainFile() {
            return mainClass() + ".java";
        }

        public List<MethodSpec> methodsOrEmpty() {
            return methods == null ? List.of() : methods;
        }
    }

    public record MethodSpec(String name, List<Param> params, String returns) {

        public String signature() {
            return returns + " " + name + "("
                    + params.stream().map(p -> p.type() + " " + p.name()).collect(Collectors.joining(", ")) + ")";
        }
    }

    public record Param(String name, String type) {}

    public record Tests(List<TestCase> visible, List<TestCase> hidden, Double tolerance) {

        public List<TestCase> visibleOrEmpty() {
            return visible == null ? List.of() : visible;
        }

        public List<TestCase> hiddenOrEmpty() {
            return hidden == null ? List.of() : hidden;
        }

        public double toleranceOrDefault() {
            return tolerance == null ? 1e-9 : tolerance;
        }
    }

    /** Either a method test ({@code args}/{@code expect}) or an input/output test ({@code stdin}/{@code stdout_*}). */
    public record TestCase(
            String name,
            String method,
            List<Object> args,
            Object expect,
            String stdin,
            String stdoutEquals,
            List<String> stdoutContains,
            List<String> sourceContains,
            List<String> sourceNotContains) {

        public boolean isMethodTest() {
            return args != null;
        }

        /**
         * A structure check on the learner's source: required and forbidden text, compared with whitespace
         * collapsed. Used for "write it in this form" and "don't use X" constraints that output can't show.
         */
        public boolean isSourceTest() {
            return sourceContains != null || sourceNotContains != null;
        }

        public boolean isIoTest() {
            return stdin != null || stdoutEquals != null || stdoutContains != null;
        }
    }

    public record Rubric(String criteria, List<RubricLevel> levels) {}

    public record RubricLevel(int score, String descriptor, List<String> samples) {}

    public record Hints(String h1, String h2) {}

    public record Limits(Integer timeMs, Integer memoryMb) {}

    public String id() {
        return spec.id();
    }

    public ExerciseType type() {
        return spec.type();
    }

    public Entry entry() {
        return spec.entry() == null ? new Entry(null, null) : spec.entry();
    }

    /** All test cases, visible first, each paired with its visibility. */
    public Stream<VisibleTest> allTests() {
        if (spec.tests() == null) {
            return Stream.empty();
        }
        return Stream.concat(
                spec.tests().visibleOrEmpty().stream().map(t -> new VisibleTest(t, true)),
                spec.tests().hiddenOrEmpty().stream().map(t -> new VisibleTest(t, false)));
    }

    public record VisibleTest(TestCase test, boolean visible) {}

    /** Parsons blocks followed by distractors; learners submit indices into this list. */
    public List<String> parsonsPalette() {
        return Stream.concat(
                spec.blocks() == null ? Stream.empty() : spec.blocks().stream(),
                spec.distractors() == null ? Stream.empty() : spec.distractors().stream()).toList();
    }
}
