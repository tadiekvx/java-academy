package academy.content;

import java.nio.file.Path;
import java.util.List;

/** A lesson file: YAML front matter plus a Markdown body. */
public record Lesson(FrontMatter meta, String body, Path file) {

    public record FrontMatter(
            String id,
            String title,
            List<String> concepts,
            List<Objective> objectives,
            List<String> prerequisites,
            Integer estimatedMinutes,
            LessonStatus status,
            List<String> authors,
            Boolean aiAssisted,
            Review technicalReview,
            Review pedagogyReview,
            List<String> sources,
            List<JavaFeature> features,
            List<String> resources) {}

    public record Objective(String id, String text) {}

    public record Review(String by, String date) {

        public boolean done() {
            return by != null && !by.isBlank() && date != null && !date.isBlank();
        }
    }

    public record JavaFeature(String name, int since) {}

    public String id() {
        return meta.id();
    }

    public LessonStatus status() {
        return meta.status();
    }
}
