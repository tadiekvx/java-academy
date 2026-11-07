package academy.api;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ResponseStatusException;

import academy.content.Content;
import academy.content.ContentRepository;
import academy.content.Exercise;
import academy.content.Lesson;

/** Decides which lessons and exercises learners may see, and looks them up for the API. */
@Component
class ContentAccess {

    private final ContentRepository repository;

    ContentAccess(ContentRepository repository) {
        this.repository = repository;
    }

    Content content() {
        return repository.content();
    }

    boolean isAvailable(Lesson lesson) {
        return repository.isAvailable(lesson);
    }

    Lesson lesson(String id) {
        return content().lesson(id).filter(this::isAvailable)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "No lesson " + id));
    }

    boolean isAvailable(academy.content.Project project) {
        return repository.isAvailable(project);
    }

    academy.content.Project project(String id) {
        return content().project(id).filter(repository::isAvailable)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "No project " + id));
    }

    Exercise exercise(String id) {
        return content().exercise(id)
                .filter(repository::isAvailable)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "No exercise " + id));
    }
}
