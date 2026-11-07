package academy.content;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Stream;

import tools.jackson.core.JacksonException;
import tools.jackson.databind.DeserializationFeature;
import tools.jackson.databind.MapperFeature;
import tools.jackson.databind.PropertyNamingStrategies;
import tools.jackson.dataformat.yaml.YAMLMapper;

/**
 * Reads the content tree ({@code curriculum.yaml}, {@code stage-N/lessons/*.md},
 * {@code stage-N/exercises/<id>/}) into a {@link Content} snapshot. Problems are collected as
 * issues instead of thrown, so that one broken file doesn't hide the rest.
 */
public final class ContentLoader {

    private static final String FRONT_MATTER_FENCE = "---";

    private final YAMLMapper yaml = YAMLMapper.builder()
            .propertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE)
            .enable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
            .enable(MapperFeature.ACCEPT_CASE_INSENSITIVE_ENUMS)
            .build();

    public Content load(Path contentRoot, Path sourcesFile) {
        List<Issue> issues = new ArrayList<>();
        Curriculum curriculum = readYaml(contentRoot.resolve("curriculum.yaml"), Curriculum.class, issues);
        if (curriculum == null) {
            curriculum = new Curriculum(null, null, List.of(), List.of(), List.of());
        }

        Map<String, Lesson> lessons = new LinkedHashMap<>();
        Map<String, Exercise> exercises = new TreeMap<>();
        Map<String, Project> projects = new TreeMap<>();
        for (Path stageDir : list(contentRoot, "stage-*")) {
            for (Path lessonFile : list(stageDir.resolve("lessons"), "*.md")) {
                Lesson lesson = readLesson(lessonFile, issues);
                if (lesson != null && lessons.putIfAbsent(lesson.id(), lesson) != null) {
                    issues.add(Issue.error(lessonFile.toString(), "Duplicate lesson id " + lesson.id()));
                }
            }
            for (Path projectDir : list(stageDir.resolve("projects"), "*")) {
                if (!Files.isDirectory(projectDir)) {
                    continue;
                }
                Project project = readProject(projectDir, issues);
                if (project != null && projects.putIfAbsent(project.id(), project) != null) {
                    issues.add(Issue.error(projectDir.toString(), "Duplicate project id " + project.id()));
                }
            }
            for (Path exerciseDir : list(stageDir.resolve("exercises"), "*")) {
                if (!Files.isDirectory(exerciseDir)) {
                    continue;
                }
                Exercise exercise = readExercise(exerciseDir, issues);
                if (exercise != null && exercises.putIfAbsent(exercise.id(), exercise) != null) {
                    issues.add(Issue.error(exerciseDir.toString(), "Duplicate exercise id " + exercise.id()));
                }
            }
        }

        Map<String, Resource> resources = readResources(contentRoot.resolve("resources.yaml"), issues);

        SourceRegister sources;
        if (Files.isRegularFile(sourcesFile)) {
            sources = SourceRegister.parse(sourcesFile);
        } else {
            issues.add(Issue.error(sourcesFile.toString(), "Source register not found"));
            sources = new SourceRegister(Map.of());
        }
        return new Content(curriculum, lessons, exercises, resources, projects, sources, List.copyOf(issues));
    }

    /** {@code resources.yaml} is optional; when present it holds a top-level {@code resources:} list. */
    private Map<String, Resource> readResources(Path file, List<Issue> issues) {
        Map<String, Resource> resources = new LinkedHashMap<>();
        if (!Files.isRegularFile(file)) {
            return resources;
        }
        ResourceFile parsed = readYaml(file, ResourceFile.class, issues);
        if (parsed != null && parsed.resources() != null) {
            for (Resource resource : parsed.resources()) {
                if (resources.putIfAbsent(resource.id(), resource) != null) {
                    issues.add(Issue.error(file.toString(), "Duplicate resource id " + resource.id()));
                }
            }
        }
        return resources;
    }

    private record ResourceFile(List<Resource> resources) {}

    private Lesson readLesson(Path file, List<Issue> issues) {
        String text = readString(file).replace("\r\n", "\n");
        if (!text.startsWith(FRONT_MATTER_FENCE + "\n")) {
            issues.add(Issue.error(file.toString(), "Lesson must start with a '---' front matter block"));
            return null;
        }
        int end = text.indexOf("\n" + FRONT_MATTER_FENCE + "\n", FRONT_MATTER_FENCE.length());
        if (end < 0) {
            issues.add(Issue.error(file.toString(), "Front matter block is not closed with '---'"));
            return null;
        }
        String frontMatter = text.substring(FRONT_MATTER_FENCE.length() + 1, end);
        String body = text.substring(end + FRONT_MATTER_FENCE.length() + 2);
        try {
            return new Lesson(yaml.readValue(frontMatter, Lesson.FrontMatter.class), body, file);
        } catch (JacksonException e) {
            issues.add(Issue.error(file.toString(), "Invalid front matter: " + e.getOriginalMessage()));
            return null;
        }
    }

    private Project readProject(Path dir, List<Issue> issues) {
        Path specFile = dir.resolve("project.yaml");
        if (!Files.isRegularFile(specFile)) {
            issues.add(Issue.error(dir.toString(), "Project directory has no project.yaml"));
            return null;
        }
        Project.Spec spec = readYaml(specFile, Project.Spec.class, issues);
        return spec == null ? null : new Project(spec, dir, readJavaFiles(dir.resolve("starter")),
                readJavaFiles(dir.resolve("solution")), readJavaFiles(dir.resolve("wrong")));
    }

    private Exercise readExercise(Path dir, List<Issue> issues) {
        Path specFile = dir.resolve("exercise.yaml");
        if (!Files.isRegularFile(specFile)) {
            issues.add(Issue.error(dir.toString(), "Exercise directory has no exercise.yaml"));
            return null;
        }
        Exercise.Spec spec = readYaml(specFile, Exercise.Spec.class, issues);
        if (spec == null) {
            return null;
        }
        return new Exercise(spec, dir, readJavaFiles(dir.resolve("starter")), readJavaFiles(dir.resolve("solution")),
                readJavaFiles(dir.resolve("wrong")));
    }

    private <T> T readYaml(Path file, Class<T> type, List<Issue> issues) {
        if (!Files.isRegularFile(file)) {
            issues.add(Issue.error(file.toString(), "File not found"));
            return null;
        }
        try {
            return yaml.readValue(readString(file), type);
        } catch (JacksonException e) {
            issues.add(Issue.error(file.toString(), "Invalid YAML: " + e.getOriginalMessage()));
            return null;
        }
    }

    private static Map<String, String> readJavaFiles(Path dir) {
        Map<String, String> files = new TreeMap<>();
        for (Path file : list(dir, "*.java")) {
            files.put(file.getFileName().toString(), readString(file));
        }
        return files;
    }

    private static List<Path> list(Path dir, String glob) {
        if (!Files.isDirectory(dir)) {
            return List.of();
        }
        try (Stream<Path> entries = Files.list(dir)) {
            var matcher = dir.getFileSystem().getPathMatcher("glob:" + glob);
            return entries.filter(p -> matcher.matches(p.getFileName())).sorted().toList();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private static String readString(Path file) {
        try {
            return Files.readString(file);
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
