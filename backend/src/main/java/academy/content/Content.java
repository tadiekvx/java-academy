package academy.content;

import java.util.List;
import java.util.Map;
import java.util.Optional;

/** A loaded snapshot of all curriculum content, plus any problems found while loading it. */
public record Content(
        Curriculum curriculum,
        Map<String, Lesson> lessons,
        Map<String, Exercise> exercises,
        Map<String, Resource> resources,
        Map<String, Project> projects,
        SourceRegister sources,
        List<Issue> loadIssues) {

    public Optional<Lesson> lesson(String id) {
        return Optional.ofNullable(lessons.get(id));
    }

    public Optional<Project> project(String id) {
        return Optional.ofNullable(projects.get(id));
    }

    /** An exercise by id, or a project milestone by its {@code projectId/milestoneId} id. */
    public Optional<Exercise> exerciseOrMilestone(String id) {
        Optional<Exercise> exercise = exercise(id);
        if (exercise.isPresent() || !id.contains("/")) {
            return exercise;
        }
        String[] parts = id.split("/", 2);
        return project(parts[0]).flatMap(p -> p.milestone(parts[1]).map(p::milestoneExercise));
    }

    public Optional<Resource> resource(String id) {
        return Optional.ofNullable(resources.get(id));
    }

    public Optional<Exercise> exercise(String id) {
        return Optional.ofNullable(exercises.get(id));
    }
}
