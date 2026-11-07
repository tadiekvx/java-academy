package academy.api;

import java.util.Map;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import academy.learner.CurrentLearner;
import academy.progress.ProgressService;

@RestController
@RequestMapping("/api")
class ProgressController {

    private final ProgressService progress;
    private final ContentAccess access;

    ProgressController(ProgressService progress, ContentAccess access) {
        this.progress = progress;
        this.access = access;
    }

    @GetMapping("/progress")
    ProgressService.ProgressView progress(Authentication authentication) {
        return progress.progress(CurrentLearner.require(authentication));
    }

    @GetMapping("/progress/lessons/{id}")
    Map<String, ProgressService.ExerciseStatus> lessonProgress(@PathVariable String id, Authentication authentication) {
        access.lesson(id);
        return progress.lessonStatus(CurrentLearner.require(authentication), id);
    }

    @PostMapping("/lessons/{id}/visit")
    void visit(@PathVariable String id, Authentication authentication) {
        access.lesson(id);
        progress.recordVisit(CurrentLearner.require(authentication), id);
    }
}
