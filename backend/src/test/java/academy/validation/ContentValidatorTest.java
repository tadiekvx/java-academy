package academy.validation;

import static org.assertj.core.api.Assertions.assertThat;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import academy.assessment.Grader;
import academy.content.ContentLoader;
import academy.content.Issue;
import academy.execution.LocalJvmRunner;

/** Checks that the gates catch broken content, by breaking a copy of the real content on purpose. */
class ContentValidatorTest {

    private static final Path REAL_CONTENT = Path.of("../content/java");
    private static final Path SOURCES = Path.of("../docs/curriculum/sources.md");
    private static final String LESSON = "stage-1/lessons/j1-l2.3.md";
    private static final String EXERCISES = "stage-1/exercises/";

    @TempDir
    Path content;

    private final ContentValidator validator = new ContentValidator(new Grader(new LocalJvmRunner()));

    @BeforeEach
    void copyRealContent() throws IOException {
        try (Stream<Path> paths = Files.walk(REAL_CONTENT)) {
            for (Path source : paths.toList()) {
                Path target = content.resolve(REAL_CONTENT.relativize(source).toString());
                if (Files.isDirectory(source)) {
                    Files.createDirectories(target);
                } else {
                    Files.copy(source, target);
                }
            }
        }
    }

    @Test
    void catchesAWrongPredictExpectedOutput() throws IOException {
        replace(EXERCISES + "j1-l2.3-predict-division/exercise.yaml", "  3.5\n", "  3\n");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("expected_output doesn't match"));
    }

    @Test
    void catchesTestsThatAcceptAKnownWrongSolution() throws IOException {
        Path wrong = content.resolve(EXERCISES + "j1-l2.3-write-average/wrong/integer-division.java");
        Files.writeString(wrong, Files.readString(wrong).replace("/ 2;", "/ 2.0;"));

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("passes every test; the tests miss it"));
    }

    @Test
    void catchesAReferenceSolutionThatFailsItsTests() throws IOException {
        replace(EXERCISES + "j1-l2.3-modify-pizza/solution/Main.java", "(slices + 5) / 6", "slices / 6");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("Reference solution does not pass"));
    }

    @Test
    void catchesPlaceholderTextInALessonUnderReview() throws IOException {
        replace(LESSON, "## Where this is used\n", "## Where this is used\n\nTODO: add examples\n");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("placeholder text 'TODO'"));
    }

    @Test
    void blocksPublishingWithoutReviewsOrWithUnverifiedSources() throws IOException {
        replace(LESSON, "status: in_review", "status: published");

        assertThat(errors())
                .anySatisfy(m -> assertThat(m).contains("without a technical review"))
                .anySatisfy(m -> assertThat(m).contains("without a pedagogy review"))
                .anySatisfy(m -> assertThat(m).contains("not yet verified"));
    }

    @Test
    void catchesAMissingRequiredSection() throws IOException {
        replace(LESSON, "## Common mistakes\n", "## Pitfalls\n");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("Missing required section '## Common mistakes'"));
    }

    @Test
    void catchesAnEmbeddedExerciseThatDoesNotExist() throws IOException {
        replace(LESSON, "::exercise{id=j1-l2.3-write-average}", "::exercise{id=j1-l2.3-write-avg}");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("Embeds unknown exercise j1-l2.3-write-avg"));
    }

    @Test
    void catchesALessonReferencingAnUnknownResource() throws IOException {
        replace("stage-1/lessons/j1-l1.1.md", "resources: [ijn-90-java-on-ramp", "resources: [made-up-video, ijn-90-java-on-ramp");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("References unknown resource made-up-video"));
    }

    @Test
    void rejectsAResourceThatWasNeverVerified() throws IOException {
        replace("resources.yaml", "    verified_on: \"2026-11-05\"\n    caveat: \"Recorded", "    caveat: \"Recorded");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("verified_on"));
    }

    @Test
    void rejectsAnEmbeddedVideoWhoseIdIsNotInItsUrl() throws IOException {
        replace("resources.yaml", "youtube_id: \"4WjXTe_FKO4\"", "youtube_id: \"AAAAAAAAAAA\"");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("youtube_id doesn't appear in the url"));
    }

    @Test
    void rejectsNonHttpsResourceUrls() throws IOException {
        replace("resources.yaml", "url: \"https://openjdk.org/jeps/512\"", "url: \"http://openjdk.org/jeps/512\"");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("URL must be https"));
    }

    @Test
    void catchesAProjectReferenceSolutionThatFailsAMilestone() throws IOException {
        replace("stage-1/projects/j1-p1-finance/solution/Main.java", "return income - totalExpenses(expenses);", "return income;");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("Reference solution does not pass this milestone"));
    }

    @Test
    void catchesAProjectWrongSolutionThatPassesItsMilestone() throws IOException {
        replace("stage-1/projects/j1-p1-finance/wrong/m2-adds.java", "return income + totalExpenses(expenses);", "return income - totalExpenses(expenses);");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("Known-wrong solution wrong/m2-adds.java passes this milestone"));
    }

    @Test
    void rejectsAProjectWithAnUnknownCategory() throws IOException {
        replace("stage-1/projects/j1-p2-receipt/project.yaml", "category: B", "category: Z");

        assertThat(errors()).anySatisfy(m -> assertThat(m).contains("category must be A, B or C"));
    }

    private void replace(String file, String from, String to) throws IOException {
        Path path = content.resolve(file);
        String text = Files.readString(path);
        assertThat(text).as("sabotage target in " + file).contains(from);
        Files.writeString(path, text.replace(from, to));
    }

    private Stream<String> errorStream() {
        return validator.validate(new ContentLoader().load(content, SOURCES)).errors().stream()
                .map(Issue::message);
    }

    private java.util.List<String> errors() {
        return errorStream().toList();
    }
}
