package academy.api;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import academy.content.Curriculum;
import academy.content.Lesson;
import academy.content.LessonStatus;

@RestController
@RequestMapping("/api")
class CurriculumController {

    private final ContentAccess access;

    CurriculumController(ContentAccess access) {
        this.access = access;
    }

    record CurriculumView(List<StageView> stages) {}

    record StageView(int number, String title, boolean optional, List<ModuleView> modules) {}

    record ModuleView(int number, String title, List<LessonSummary> lessons) {}

    record LessonSummary(String id, String title, boolean available, LessonStatus status) {}

    record LessonView(
            String id,
            String title,
            List<Lesson.Objective> objectives,
            Integer estimatedMinutes,
            LessonStatus status,
            String body,
            List<ResourceView> resources) {}

    record ResourceView(
            String id,
            String title,
            String creator,
            String url,
            String kind,
            String level,
            String topic,
            String why,
            String embedUrl,
            String published,
            String caveat) {}

    @GetMapping("/curriculum")
    CurriculumView curriculum() {
        Curriculum curriculum = access.content().curriculum();
        return new CurriculumView(curriculum.stages().stream()
                .map(stage -> new StageView(stage.number(), stage.title(), stage.isOptional(), stage.modules().stream()
                        .map(module -> new ModuleView(module.number(), module.title(), module.lessons().stream()
                                .map(this::summarise).toList()))
                        .toList()))
                .toList());
    }

    @GetMapping("/lessons/{id}")
    LessonView lesson(@PathVariable String id) {
        Lesson lesson = access.lesson(id);
        var meta = lesson.meta();
        List<ResourceView> resources = (meta.resources() == null ? List.<String>of() : meta.resources()).stream()
                .flatMap(resourceId -> access.content().resource(resourceId).stream())
                .map(CurriculumController::view)
                .toList();
        return new LessonView(meta.id(), meta.title(), meta.objectives(), meta.estimatedMinutes(), meta.status(), lesson.body(),
                resources);
    }

    private static ResourceView view(academy.content.Resource r) {
        // Privacy-friendly embed host; the start offset is the verified timestamp, if one was recorded.
        String embed = r.embeddable()
                ? "https://www.youtube-nocookie.com/embed/" + r.youtubeId() + (r.startSeconds() == null ? "" : "?start=" + r.startSeconds())
                : null;
        return new ResourceView(r.id(), r.title(), r.creator(), r.url(), r.kind().label(), r.level().name().toLowerCase(), r.topic(),
                r.why(), embed, r.published(), r.caveat());
    }

    private LessonSummary summarise(Curriculum.LessonOutline outline) {
        return access.content().lesson(outline.id())
                .map(lesson -> new LessonSummary(outline.id(), outline.title(), access.isAvailable(lesson), lesson.status()))
                .orElseGet(() -> new LessonSummary(outline.id(), outline.title(), false, null));
    }
}
