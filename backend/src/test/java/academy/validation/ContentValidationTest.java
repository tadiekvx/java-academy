package academy.validation;

import static org.assertj.core.api.Assertions.assertThat;

import java.nio.file.Path;

import org.junit.jupiter.api.Test;

import academy.assessment.Grader;
import academy.content.Content;
import academy.content.ContentLoader;
import academy.execution.LocalJvmRunner;

/**
 * The automated publication gate: validates the repository's real content and fails the build on
 * any error. Warnings are printed but don't fail the build.
 */
class ContentValidationTest {

    @Test
    void repositoryContentPassesAllGates() {
        Content content = new ContentLoader().load(Path.of("../content/java"), Path.of("../docs/curriculum/sources.md"));
        ValidationReport report = new ContentValidator(new Grader(new LocalJvmRunner())).validate(content);

        System.out.println(report.format());
        assertThat(report.errors()).as(report.format()).isEmpty();
    }
}
