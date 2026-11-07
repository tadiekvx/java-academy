package academy.api;

import java.util.Comparator;
import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import academy.assessment.GradeReport;
import academy.assessment.Grader;
import academy.assessment.Submission;
import academy.assessment.TestDescriptions;
import academy.content.Exercise;
import academy.content.Project;
import academy.learner.CurrentLearner;
import academy.progress.AttemptContext;
import academy.progress.ProgressService;

/**
 * Projects: larger programs built in milestones. The learner edits one file; each milestone has its own
 * tests. Hidden tests and the reference solution never leave the server.
 */
@RestController
@RequestMapping("/api")
class ProjectController {

    private final ContentAccess access;
    private final Grader grader;
    private final ProgressService progress;

    ProjectController(ContentAccess access, Grader grader, ProgressService progress) {
        this.access = access;
        this.grader = grader;
        this.progress = progress;
    }

    record ProjectSummary(String id, String title, String category, String summary, Integer estimatedHours, int milestones,
            String status) {}

    record MilestoneView(String id, String title, String instructions, List<String> signatures, List<TestView> visibleTests) {}

    record TestView(String name, String call, String expected) {}

    record RubricView(String criterion, String zero, String one, String two) {}

    record ProjectView(
            String id,
            String title,
            String category,
            String status,
            String summary,
            String brief,
            Integer estimatedHours,
            List<String> prerequisites,
            List<String> requirements,
            List<String> constraints,
            List<String> acceptance,
            List<MilestoneView> milestones,
            List<RubricView> rubric,
            String designNotePrompt,
            Map<String, String> files) {}

    @GetMapping("/projects")
    List<ProjectSummary> projects() {
        return access.content().projects().values().stream()
                .filter(p -> access.isAvailable(p))
                .sorted(Comparator.comparing((Project p) -> p.spec().category()).thenComparing(Project::id))
                .map(p -> new ProjectSummary(p.id(), p.spec().title(), p.spec().category(), p.spec().summary(),
                        p.spec().estimatedHours(), p.spec().milestones().size(), p.status().name()))
                .toList();
    }

    @GetMapping("/projects/{id}")
    ProjectView project(@PathVariable String id) {
        Project project = access.project(id);
        Project.Spec spec = project.spec();
        List<MilestoneView> milestones = spec.milestones().stream().map(m -> {
            Exercise exercise = project.milestoneExercise(m);
            List<TestView> visible = m.tests().visibleOrEmpty().stream()
                    .map(t -> new TestView(t.name(), TestDescriptions.call(exercise, t), TestDescriptions.expected(t))).toList();
            return new MilestoneView(m.id(), m.title(), m.instructions(),
                    exercise.entry().methodsOrEmpty().stream().map(Exercise.MethodSpec::signature).toList(), visible);
        }).toList();
        return new ProjectView(spec.id(), spec.title(), spec.category(), spec.status().name(), spec.summary(), spec.brief(),
                spec.estimatedHours(), orEmpty(spec.prerequisites()), orEmpty(spec.requirements()), orEmpty(spec.constraints()),
                orEmpty(spec.acceptance()), milestones,
                orEmpty(spec.rubric()).stream().map(r -> new RubricView(r.criterion(), r.zero(), r.one(), r.two())).toList(),
                spec.designNotePrompt(), project.starter());
    }

    @PostMapping("/projects/{id}/milestones/{milestoneId}/attempts")
    GradeReport attempt(@PathVariable String id, @PathVariable String milestoneId, @RequestBody Submission submission,
            Authentication authentication) {
        long learnerId = CurrentLearner.require(authentication);
        Project project = access.project(id);
        Project.Milestone milestone = project.milestone(milestoneId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "No milestone " + milestoneId));
        Exercise exercise = project.milestoneExercise(milestone);
        GradeReport report = grader.grade(exercise, submission);
        // The mentor does not support projects yet, so project attempts record no assistance.
        progress.recordAttempt(learnerId, exercise, submission, report, AttemptContext.PRACTICE, 0, false);
        return report.forLearner();
    }

    @GetMapping("/progress/projects/{id}")
    Map<String, ProgressService.ExerciseStatus> status(@PathVariable String id, Authentication authentication) {
        return progress.projectStatus(CurrentLearner.require(authentication), access.project(id));
    }

    private static <T> List<T> orEmpty(List<T> list) {
        return list == null ? List.of() : list;
    }
}
