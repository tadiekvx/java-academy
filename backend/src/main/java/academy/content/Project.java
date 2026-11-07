package academy.content;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

/**
 * A project (docs/curriculum/01-curriculum-design.md §3): a larger program built in milestones.
 * The learner works in one file; each milestone is checked by its own tests, which are the same
 * kind of tests exercises use. Category A is guided, B gives requirements only, C simulates
 * professional work on an existing codebase.
 */
public record Project(Spec spec, Path dir, Map<String, String> starter, Map<String, String> solution, Map<String, String> wrong) {

    public record Spec(
            String id,
            String title,
            String category,
            LessonStatus status,
            String summary,
            String brief,
            Integer estimatedHours,
            List<String> prerequisites,
            List<String> concepts,
            List<String> requirements,
            List<String> constraints,
            List<String> acceptance,
            List<Milestone> milestones,
            List<RubricCriterion> rubric,
            String designNotePrompt,
            Boolean aiAssisted) {}

    public record Milestone(String id, String title, String instructions, Exercise.Entry entry, Exercise.Tests tests) {}

    public record RubricCriterion(String criterion, String zero, String one, String two) {}

    public String id() {
        return spec.id();
    }

    public LessonStatus status() {
        return spec.status();
    }

    /** The evidence type a passing milestone gives: guided builds practise, independent work transfers. */
    public Evidence evidence() {
        return "A".equals(spec.category()) ? Evidence.IMPL : Evidence.XFER;
    }

    public static String milestoneExerciseId(String projectId, String milestoneId) {
        return projectId + "/" + milestoneId;
    }

    /** A milestone viewed as an exercise, so the grader and the mastery model can treat it uniformly. */
    public Exercise milestoneExercise(Milestone milestone) {
        var exerciseSpec = new Exercise.Spec(
                milestoneExerciseId(id(), milestone.id()), ExerciseType.WRITE, milestone.title(), id(), Exercise.Role.LADDER,
                List.of(), spec.concepts() == null ? List.of() : spec.concepts(), List.of(evidence()), List.of(), 3, null,
                milestone.instructions(), milestone.entry(), milestone.tests(), null, null, null, null, null, null, null, null, false);
        return new Exercise(exerciseSpec, dir, starter, solution, wrong);
    }

    public java.util.Optional<Milestone> milestone(String milestoneId) {
        return spec.milestones().stream().filter(m -> m.id().equals(milestoneId)).findFirst();
    }
}
