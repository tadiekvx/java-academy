package academy.content;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

/** Holds the current content snapshot, loaded from disk at startup. */
@Component
public class ContentRepository {

    private static final Logger log = LoggerFactory.getLogger(ContentRepository.class);

    private final ContentProperties properties;
    private volatile Content content;

    public ContentRepository(ContentProperties properties) {
        this.properties = properties;
        reload();
    }

    public Content content() {
        return content;
    }

    /** Whether learners may see the lesson: it is published, or this is a reviewer/development setup. */
    public boolean isAvailable(Lesson lesson) {
        return lesson.status() == LessonStatus.PUBLISHED
                || (properties.showUnpublished() && lesson.status() != LessonStatus.RETIRED);
    }

    /** Whether learners may see the project. */
    public boolean isAvailable(Project project) {
        return project.status() == LessonStatus.PUBLISHED
                || (properties.showUnpublished() && project.status() != LessonStatus.RETIRED);
    }

    /** Whether learners may see the exercise, which follows its lesson. */
    public boolean isAvailable(Exercise exercise) {
        return content.lesson(exercise.spec().lesson()).filter(this::isAvailable).isPresent();
    }

    public void reload() {
        Content loaded = new ContentLoader().load(properties.rootPath(), properties.sourcesPath());
        loaded.loadIssues().forEach(issue -> log.warn("Content {}: {} — {}", issue.severity(), issue.location(), issue.message()));
        log.info("Loaded {} lessons and {} exercises from {}",
                loaded.lessons().size(), loaded.exercises().size(), properties.rootPath().toAbsolutePath().normalize());
        content = loaded;
    }
}
