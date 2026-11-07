package academy.content;

import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

/** The curriculum outline from {@code curriculum.yaml}: concepts, misconceptions and the stage structure. */
public record Curriculum(
        String track,
        Integer javaVersion,
        List<Concept> concepts,
        List<Misconception> misconceptions,
        List<Stage> stages) {

    /** An {@code optional} stage is never the "continue" recommendation unless the learner has already opened one of its lessons. */
    public record Stage(int number, String title, Boolean optional, List<Module> modules) {

        public boolean isOptional() {
            return Boolean.TRUE.equals(optional);
        }
    }

    public record Module(int number, String title, List<LessonOutline> lessons) {}

    public record LessonOutline(String id, String title, List<String> concepts) {}

    public Stream<LessonOutline> lessonOutlines() {
        return stages.stream().flatMap(s -> s.modules().stream()).flatMap(m -> m.lessons().stream());
    }

    public Optional<LessonOutline> lessonOutline(String id) {
        return lessonOutlines().filter(l -> l.id().equals(id)).findFirst();
    }

    public Optional<Concept> concept(String id) {
        return concepts.stream().filter(c -> c.id().equals(id)).findFirst();
    }

    public Optional<Misconception> misconception(String id) {
        return misconceptions.stream().filter(m -> m.id().equals(id)).findFirst();
    }
}
