package academy.validation;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import org.springframework.stereotype.Component;

import academy.assessment.GradeReport;
import academy.assessment.Grader;
import academy.assessment.Submission;
import academy.content.Concept;
import academy.content.Content;
import academy.content.Curriculum;
import academy.content.Exercise;
import academy.content.Exercise.MethodSpec;
import academy.content.Issue;
import academy.content.Lesson;
import academy.content.LessonStatus;
import academy.content.Misconception;
import academy.content.Project;
import academy.content.Resource;

/**
 * Applies the automated publication gates from docs/curriculum/03-content-standards.md §6.
 *
 * <p>Correctness problems (a reference solution that fails its tests, a broken reference) are
 * always errors. Publication-standard problems (missing sections, unverified sources, missing
 * reviews, placeholder text) are errors for lessons in review or published, and warnings for drafts.
 */
@Component
public class ContentValidator {

    static final List<String> REQUIRED_SECTIONS = List.of(
            "Before you start", "Explanation", "Worked examples", "Where this is used", "Common mistakes",
            "Practice", "Further reading", "How you'll be assessed");
    private static final int MIN_VISIBLE_TESTS = 3;
    private static final int MIN_HIDDEN_TESTS = 5;
    private static final int MIN_VARIANT_GROUP_SIZE = 3;

    private static final Pattern PLACEHOLDER = Pattern.compile("\\b(TODO|TBD|FIXME|XXX|lorem ipsum|placeholder)\\b",
            Pattern.CASE_INSENSITIVE);
    private static final Pattern HEADING = Pattern.compile("^## (.+?)\\s*$", Pattern.MULTILINE);
    private static final Pattern EXERCISE_DIRECTIVE = Pattern.compile("^::exercise\\{id=([\\w.-]+)}\\s*$", Pattern.MULTILINE);
    private static final Pattern MISTAKE_DIRECTIVE = Pattern.compile("^:::mistake\\{id=(\\w+)}\\s*$", Pattern.MULTILINE);
    private static final Pattern RUNNABLE = Pattern.compile("^```java runnable\\n(.*?)^```\\s*$", Pattern.MULTILINE | Pattern.DOTALL);

    private final Grader grader;

    public ContentValidator(Grader grader) {
        this.grader = grader;
    }

    public ValidationReport validate(Content content) {
        List<Issue> issues = new ArrayList<>(content.loadIssues());
        validateCurriculum(content.curriculum(), issues);
        for (Lesson lesson : content.lessons().values()) {
            validateLesson(lesson, content, issues);
        }
        for (Exercise exercise : content.exercises().values()) {
            validateExercise(exercise, content, issues);
        }
        validateVariantGroups(content, issues);
        validateResources(content, issues);
        for (Project project : content.projects().values()) {
            validateProject(project, content, issues);
        }
        return new ValidationReport(issues);
    }

    private static final Pattern YOUTUBE_ID = Pattern.compile("[A-Za-z0-9_-]{11}");
    private static final Pattern ISO_DATE = Pattern.compile("\\d{4}-\\d{2}-\\d{2}");

    /**
     * Resources must be real and traceable: complete metadata, an https URL, the date someone opened it
     * and confirmed it, and for embedded videos an id that matches the URL. Resources no lesson uses
     * are reported as warnings.
     */
    private void validateResources(Content content, List<Issue> issues) {
        Set<String> used = new HashSet<>();
        for (Lesson lesson : content.lessons().values()) {
            for (String id : orEmpty(lesson.meta().resources())) {
                used.add(id);
                if (content.resource(id).isEmpty()) {
                    issues.add(Issue.error("lesson " + lesson.id(), "References unknown resource " + id));
                }
            }
        }
        for (Resource r : content.resources().values()) {
            String where = "resource " + r.id();
            requireText(r.title(), "title", where, issues);
            requireText(r.creator(), "creator", where, issues);
            requireText(r.topic(), "topic", where, issues);
            requireText(r.why(), "why (why it is recommended)", where, issues);
            if (r.kind() == null || r.level() == null) {
                issues.add(Issue.error(where, "Needs kind and level"));
            }
            if (r.url() == null || !r.url().startsWith("https://")) {
                issues.add(Issue.error(where, "URL must be https"));
            }
            if (r.verifiedOn() == null || !ISO_DATE.matcher(r.verifiedOn()).matches()) {
                issues.add(Issue.error(where, "verified_on (yyyy-mm-dd) is required: someone must have opened the URL"));
            }
            if (r.youtubeId() != null) {
                if (!YOUTUBE_ID.matcher(r.youtubeId()).matches()) {
                    issues.add(Issue.error(where, "youtube_id is not a valid 11-character id"));
                } else if (r.url() == null || !r.url().contains(r.youtubeId())) {
                    issues.add(Issue.error(where, "youtube_id doesn't appear in the url"));
                }
                if (r.kind() != Resource.Kind.VIDEO) {
                    issues.add(Issue.error(where, "Only videos may have a youtube_id"));
                }
            }
            if (r.startSeconds() != null && (r.startSeconds() < 0 || r.youtubeId() == null)) {
                issues.add(Issue.error(where, "start_seconds needs a youtube_id and must not be negative"));
            }
            if (!used.contains(r.id())) {
                issues.add(Issue.warning(where, "Not used by any lesson"));
            }
        }
    }

    /**
     * Projects follow the same rules as exercises, per milestone: the reference solution passes every
     * milestone, the starter passes none, and each known-wrong solution (named {@code <milestone>-<name>.java})
     * fails the milestone it is named for. Category B and C projects must give requirements, acceptance
     * criteria, a rubric and a design-note prompt; category A projects must give instructions per milestone.
     */
    private void validateProject(Project project, Content content, List<Issue> issues) {
        Project.Spec spec = project.spec();
        String where = "project " + (spec.id() == null ? project.dir() : spec.id());
        if (spec.id() == null || spec.milestones() == null || spec.milestones().isEmpty()) {
            issues.add(Issue.error(where, "A project needs an id and at least one milestone"));
            return;
        }
        Issue.Severity standard = standardSeverity(spec.status() == null ? LessonStatus.DRAFT : spec.status());
        if (!project.dir().getFileName().toString().equals(spec.id())) {
            issues.add(Issue.error(where, "Directory name must match the project id"));
        }
        requireText(spec.title(), "title", where, issues);
        requireText(spec.summary(), "summary", where, issues);
        requireText(spec.brief(), "brief", where, issues);
        if (spec.status() == null) {
            issues.add(Issue.error(where, "Missing status"));
        }
        if (spec.category() == null || !List.of("A", "B", "C").contains(spec.category())) {
            issues.add(Issue.error(where, "category must be A, B or C"));
        }
        for (String lesson : orEmpty(spec.prerequisites())) {
            if (content.lesson(lesson).isEmpty() && content.curriculum().lessonOutline(lesson).isEmpty()) {
                issues.add(Issue.error(where, "Unknown prerequisite lesson " + lesson));
            }
        }
        for (String concept : orEmpty(spec.concepts())) {
            if (content.curriculum().concept(concept).isEmpty()) {
                issues.add(Issue.error(where, "Unknown concept " + concept));
            }
        }
        if (!"A".equals(spec.category())) {
            if (orEmpty(spec.requirements()).isEmpty() || orEmpty(spec.acceptance()).isEmpty()) {
                issues.add(Issue.error(where, "Category B and C projects need requirements and acceptance criteria"));
            }
            if (orEmpty(spec.rubric()).size() < 3) {
                issues.add(Issue.error(where, "Category B and C projects need a rubric of at least 3 criteria"));
            }
            requireText(spec.designNotePrompt(), "design_note_prompt", where, issues);
        }
        checkPlaceholders(spec.brief() == null ? "" : spec.brief(), where, standard, issues);
        String mainFile = "Main.java";
        if (!project.starter().containsKey(mainFile) || !project.solution().containsKey(mainFile)) {
            issues.add(Issue.error(where, "Needs starter/Main.java and solution/Main.java"));
            return;
        }
        Set<String> milestoneIds = new HashSet<>();
        for (Project.Milestone milestone : spec.milestones()) {
            String mWhere = where + " milestone " + milestone.id();
            if (milestone.id() == null || !milestoneIds.add(milestone.id())) {
                issues.add(Issue.error(mWhere, "Missing or duplicate milestone id"));
                continue;
            }
            requireText(milestone.title(), "title", mWhere, issues);
            requireText(milestone.instructions(), "instructions", mWhere, issues);
            Exercise exercise = project.milestoneExercise(milestone);
            if (!checkTests(exercise, mWhere, issues)) {
                continue;
            }
            GradeReport solution = grade(exercise, project.solution(), mWhere, issues);
            if (solution != null && !solution.passed()) {
                issues.add(Issue.error(mWhere, "Reference solution does not pass this milestone: " + summarise(solution)));
            }
            GradeReport starter = grade(exercise, project.starter(), mWhere, issues);
            if (starter != null && starter.passed()) {
                issues.add(Issue.error(mWhere, "Starter already passes this milestone"));
            }
            if (starter != null && starter.outcome() == GradeReport.Outcome.COMPILE_ERROR) {
                issues.add(Issue.error(mWhere, "Starter must compile (use stubs): " + starter.diagnostics()));
            }
            boolean hasWrong = false;
            for (var wrong : project.wrong().entrySet()) {
                if (!wrong.getKey().startsWith(milestone.id() + "-")) {
                    continue;
                }
                hasWrong = true;
                GradeReport report = grade(exercise, Map.of(mainFile, wrong.getValue()), mWhere, issues);
                if (report != null && report.passed()) {
                    issues.add(Issue.error(mWhere, "Known-wrong solution wrong/" + wrong.getKey() + " passes this milestone"));
                }
            }
            if (!hasWrong) {
                issues.add(new Issue(standard, mWhere, "Needs a known-wrong solution named wrong/" + milestone.id() + "-<name>.java"));
            }
        }
        for (String wrongName : project.wrong().keySet()) {
            if (milestoneIds.stream().noneMatch(id -> wrongName.startsWith(id + "-"))) {
                issues.add(Issue.error(where, "wrong/" + wrongName + " doesn't start with a milestone id"));
            }
        }
    }

    private void validateCurriculum(Curriculum curriculum, List<Issue> issues) {
        String where = "curriculum.yaml";
        Set<String> conceptIds = new HashSet<>();
        for (Concept concept : curriculum.concepts()) {
            if (!conceptIds.add(concept.id())) {
                issues.add(Issue.error(where, "Duplicate concept " + concept.id()));
            }
            if (concept.requiredEvidence() == null || concept.requiredEvidence().isEmpty()) {
                issues.add(Issue.error(where, "Concept " + concept.id() + " has no required evidence"));
            }
        }
        for (Concept concept : curriculum.concepts()) {
            for (String prerequisite : orEmpty(concept.prerequisites())) {
                if (!conceptIds.contains(prerequisite)) {
                    issues.add(Issue.error(where, "Concept " + concept.id() + " has unknown prerequisite " + prerequisite));
                }
            }
        }
        for (Misconception misconception : curriculum.misconceptions()) {
            for (String concept : orEmpty(misconception.concepts())) {
                if (!conceptIds.contains(concept)) {
                    issues.add(Issue.error(where, "Misconception " + misconception.id() + " has unknown concept " + concept));
                }
            }
        }
        Set<String> lessonIds = new HashSet<>();
        curriculum.lessonOutlines().forEach(outline -> {
            if (!lessonIds.add(outline.id())) {
                issues.add(Issue.error(where, "Duplicate lesson " + outline.id()));
            }
            for (String concept : orEmpty(outline.concepts())) {
                if (!conceptIds.contains(concept)) {
                    issues.add(Issue.error(where, "Lesson " + outline.id() + " has unknown concept " + concept));
                }
            }
        });
    }

    private void validateLesson(Lesson lesson, Content content, List<Issue> issues) {
        Lesson.FrontMatter meta = lesson.meta();
        String where = "lesson " + (meta.id() == null ? lesson.file() : meta.id());
        if (meta.id() == null || meta.status() == null) {
            issues.add(Issue.error(where, "Front matter needs at least id and status"));
            return;
        }
        Issue.Severity standard = standardSeverity(meta.status());
        Curriculum curriculum = content.curriculum();

        if (curriculum.lessonOutline(meta.id()).isEmpty()) {
            issues.add(Issue.error(where, "Not listed in curriculum.yaml"));
        }
        requireText(meta.title(), "title", where, issues);
        if (meta.estimatedMinutes() == null) {
            issues.add(Issue.error(where, "Missing estimated_minutes"));
        }
        if (meta.aiAssisted() == null) {
            issues.add(Issue.error(where, "Missing ai_assisted (declare whether any part was drafted with AI)"));
        }
        if (orEmpty(meta.authors()).isEmpty()) {
            issues.add(Issue.error(where, "Missing authors"));
        }
        if (orEmpty(meta.concepts()).isEmpty()) {
            issues.add(Issue.error(where, "Lists no concepts"));
        }
        for (String concept : orEmpty(meta.concepts())) {
            if (curriculum.concept(concept).isEmpty()) {
                issues.add(Issue.error(where, "Unknown concept " + concept));
            }
        }
        for (String prerequisite : orEmpty(meta.prerequisites())) {
            if (curriculum.lessonOutline(prerequisite).isEmpty()) {
                issues.add(Issue.error(where, "Unknown prerequisite lesson " + prerequisite));
            }
        }
        if (orEmpty(meta.objectives()).isEmpty()) {
            issues.add(Issue.error(where, "Has no learning objectives"));
        }
        Set<String> objectiveIds = new HashSet<>();
        for (Lesson.Objective objective : orEmpty(meta.objectives())) {
            if (!objectiveIds.add(objective.id())) {
                issues.add(Issue.error(where, "Duplicate objective id " + objective.id()));
            }
        }

        if (orEmpty(meta.sources()).isEmpty()) {
            issues.add(new Issue(standard, where, "Cites no sources"));
        }
        for (String source : orEmpty(meta.sources())) {
            content.sources().isVerified(source).ifPresentOrElse(
                    verified -> {
                        if (!verified) {
                            issues.add(new Issue(meta.status() == LessonStatus.PUBLISHED ? Issue.Severity.ERROR : Issue.Severity.WARNING,
                                    where, "Cites source " + source + ", which is not yet verified in the source register"));
                        }
                    },
                    () -> issues.add(Issue.error(where, "Cites unknown source " + source)));
        }
        if (meta.status() == LessonStatus.PUBLISHED) {
            if (meta.technicalReview() == null || !meta.technicalReview().done()) {
                issues.add(Issue.error(where, "Published without a technical review"));
            }
            if (meta.pedagogyReview() == null || !meta.pedagogyReview().done()) {
                issues.add(Issue.error(where, "Published without a pedagogy review"));
            }
        }

        Set<String> headings = new HashSet<>();
        HEADING.matcher(lesson.body()).results().forEach(m -> headings.add(m.group(1)));
        for (String section : REQUIRED_SECTIONS) {
            if (!headings.contains(section)) {
                issues.add(new Issue(standard, where, "Missing required section '## " + section + "'"));
            }
        }
        checkPlaceholders(lesson.body(), where, standard, issues);

        Set<String> referenced = new LinkedHashSet<>();
        EXERCISE_DIRECTIVE.matcher(lesson.body()).results().forEach(m -> referenced.add(m.group(1)));
        for (String id : referenced) {
            content.exercise(id).ifPresentOrElse(
                    exercise -> {
                        if (!meta.id().equals(exercise.spec().lesson())) {
                            issues.add(Issue.error(where, "Embeds exercise " + id + ", which belongs to lesson " + exercise.spec().lesson()));
                        }
                    },
                    () -> issues.add(Issue.error(where, "Embeds unknown exercise " + id)));
        }
        List<Exercise> ownExercises = content.exercises().values().stream()
                .filter(e -> meta.id().equals(e.spec().lesson())).toList();
        for (Exercise exercise : ownExercises) {
            if (exercise.spec().role() != Exercise.Role.RETRIEVAL && !referenced.contains(exercise.id())) {
                issues.add(Issue.warning(where, "Ladder exercise " + exercise.id() + " is not embedded in the lesson"));
            }
        }
        for (Lesson.Objective objective : orEmpty(meta.objectives())) {
            boolean assessed = ownExercises.stream().anyMatch(e -> orEmpty(e.spec().assesses()).contains(objective.id()));
            if (!assessed) {
                issues.add(new Issue(standard, where, "Objective " + objective.id() + " is not assessed by any exercise"));
            }
        }

        MISTAKE_DIRECTIVE.matcher(lesson.body()).results().forEach(m -> {
            if (curriculum.misconception(m.group(1)).isEmpty()) {
                issues.add(Issue.error(where, "Unknown misconception " + m.group(1)));
            }
        });

        Matcher snippets = RUNNABLE.matcher(lesson.body());
        int snippetNumber = 0;
        while (snippets.find()) {
            snippetNumber++;
            Grader.ProgramRun run = grader.runProgram(Map.of("Main.java", snippets.group(1)), "Main", "");
            if (!run.compiled()) {
                issues.add(Issue.error(where, "Runnable snippet " + snippetNumber + " doesn't compile: " + run.diagnostics()));
            } else if (!run.result().completedNormally()) {
                issues.add(Issue.error(where, "Runnable snippet " + snippetNumber + " doesn't run cleanly: " + run.result().stderr()));
            }
        }
    }

    private void validateExercise(Exercise exercise, Content content, List<Issue> issues) {
        Exercise.Spec spec = exercise.spec();
        String where = "exercise " + (spec.id() == null ? exercise.dir() : spec.id());
        if (spec.id() == null || spec.type() == null) {
            issues.add(Issue.error(where, "exercise.yaml needs at least id and type"));
            return;
        }
        if (!exercise.dir().getFileName().toString().equals(spec.id())) {
            issues.add(Issue.error(where, "Directory name must match the exercise id"));
        }
        Lesson lesson = spec.lesson() == null ? null : content.lesson(spec.lesson()).orElse(null);
        LessonStatus status = lesson == null ? LessonStatus.DRAFT : lesson.status();
        Issue.Severity standard = standardSeverity(status);
        Curriculum curriculum = content.curriculum();

        requireText(spec.title(), "title", where, issues);
        requireText(spec.prompt(), "prompt", where, issues);
        if (spec.lesson() == null || curriculum.lessonOutline(spec.lesson()).isEmpty()) {
            issues.add(Issue.error(where, "Must belong to a lesson listed in curriculum.yaml"));
        } else if (lesson == null) {
            issues.add(Issue.warning(where, "Its lesson " + spec.lesson() + " has not been written yet"));
        }
        if (spec.role() == null) {
            issues.add(Issue.error(where, "Missing role (ladder or retrieval)"));
        }
        if (spec.difficulty() == null || spec.difficulty() < 1 || spec.difficulty() > 5) {
            issues.add(Issue.error(where, "difficulty must be 1–5"));
        }
        if (orEmpty(spec.concepts()).isEmpty() || orEmpty(spec.evidence()).isEmpty()) {
            issues.add(Issue.error(where, "Every exercise must declare at least one concept and one evidence type"));
        }
        for (String concept : orEmpty(spec.concepts())) {
            if (curriculum.concept(concept).isEmpty()) {
                issues.add(Issue.error(where, "Unknown concept " + concept));
            }
        }
        for (String misconception : orEmpty(spec.misconceptions())) {
            if (curriculum.misconception(misconception).isEmpty()) {
                issues.add(Issue.error(where, "Unknown misconception " + misconception));
            }
        }
        if (orEmpty(spec.assesses()).isEmpty()) {
            issues.add(Issue.error(where, "Must assess at least one lesson objective"));
        }
        if (lesson != null) {
            Set<String> objectives = orEmpty(lesson.meta().objectives()).stream().map(Lesson.Objective::id).collect(Collectors.toSet());
            for (String objective : orEmpty(spec.assesses())) {
                if (!objectives.contains(objective)) {
                    issues.add(Issue.error(where, "Assesses unknown objective " + objective + " of lesson " + lesson.id()));
                }
            }
        }
        checkPlaceholders(spec.prompt() == null ? "" : spec.prompt(), where, standard, issues);

        switch (spec.type()) {
            case WRITE, DEBUG, MODIFY -> validateCodeExercise(exercise, where, standard, issues);
            case PARSONS -> validateParsons(exercise, where, issues);
            case PREDICT -> validatePredict(exercise, where, issues);
            case EXPLAIN -> validateExplain(exercise, content, where, issues);
        }
    }

    private void validateCodeExercise(Exercise exercise, String where, Issue.Severity standard, List<Issue> issues) {
        Exercise.Spec spec = exercise.spec();
        if (!checkTests(exercise, where, issues)) {
            return;
        }
        String mainFile = exercise.entry().mainFile();
        if (!exercise.starter().containsKey(mainFile) || !exercise.solution().containsKey(mainFile)) {
            issues.add(Issue.error(where, "Needs starter/" + mainFile + " and solution/" + mainFile));
            return;
        }
        if (takesInput(exercise)) {
            if (spec.tests().visibleOrEmpty().size() < MIN_VISIBLE_TESTS || spec.tests().hiddenOrEmpty().size() < MIN_HIDDEN_TESTS) {
                issues.add(Issue.error(where, "Needs at least " + MIN_VISIBLE_TESTS + " visible and " + MIN_HIDDEN_TESTS + " hidden tests"));
            }
        } else {
            // A program without input, or a method without parameters, behaves the same every run: one
            // exact check per behaviour is complete coverage.
            for (MethodSpec method : exercise.entry().methodsOrEmpty()) {
                boolean tested = exercise.allTests().anyMatch(t -> t.test().isMethodTest()
                        && method.name().equals(t.test().method() == null ? exercise.entry().methodsOrEmpty().getFirst().name() : t.test().method()));
                if (!tested) {
                    issues.add(Issue.error(where, "Method " + method.name() + " has no test"));
                }
            }
            boolean hasIoTests = exercise.allTests().anyMatch(t -> t.test().isIoTest());
            if (hasIoTests && exercise.allTests().noneMatch(t -> t.test().stdoutEquals() != null)) {
                issues.add(Issue.error(where, "A program without input needs a stdout_equals test that checks its whole output"));
            }
        }
        if (exercise.wrong().isEmpty()) {
            issues.add(Issue.error(where, "Needs at least one known-wrong solution in wrong/"));
        }
        if (spec.hints() == null || spec.hints().h1() == null || spec.hints().h2() == null) {
            issues.add(new Issue(standard, where, "Needs authored hints h1 and h2 (the mentor's grounding)"));
        }

        GradeReport solution = grade(exercise, exercise.solution(), where, issues);
        if (solution == null) {
            return;
        }
        if (!solution.passed()) {
            issues.add(Issue.error(where, "Reference solution does not pass its tests: " + summarise(solution)));
        }

        GradeReport starter = grade(exercise, exercise.starter(), where, issues);
        if (starter != null) {
            boolean shouldCompile = spec.starterCompiles() == null || spec.starterCompiles();
            boolean compiles = starter.outcome() != GradeReport.Outcome.COMPILE_ERROR;
            if (shouldCompile != compiles) {
                issues.add(Issue.error(where, shouldCompile
                        ? "Starter code doesn't compile (set starter_compiles: false if that's intended): " + starter.diagnostics()
                        : "Starter code compiles, but starter_compiles is false"));
            }
            if (starter.passed()) {
                issues.add(Issue.error(where, "Starter code already passes every test"));
            }
        }

        for (var wrong : exercise.wrong().entrySet()) {
            GradeReport report = grade(exercise, Map.of(mainFile, wrong.getValue()), where, issues);
            if (report != null && report.passed()) {
                issues.add(Issue.error(where, "Known-wrong solution wrong/" + wrong.getKey() + " passes every test; the tests miss it"));
            }
        }
    }

    /** Whether any test gives the code input: method arguments, or text on standard input. */
    private static boolean takesInput(Exercise exercise) {
        return exercise.allTests().anyMatch(t -> (t.test().isMethodTest() && !t.test().args().isEmpty())
                || (t.test().isIoTest() && t.test().stdin() != null && !t.test().stdin().isEmpty()));
    }

    private void validateParsons(Exercise exercise, String where, List<Issue> issues) {
        List<String> blocks = orEmpty(exercise.spec().blocks());
        if (blocks.isEmpty()) {
            issues.add(Issue.error(where, "Parsons exercise has no blocks"));
            return;
        }
        if (!checkTests(exercise, where, issues)) {
            return;
        }
        List<Integer> listedOrder = java.util.stream.IntStream.range(0, blocks.size()).boxed().toList();
        GradeReport report = grader.grade(exercise, new Submission(null, null, listedOrder, null));
        if (!report.passed()) {
            issues.add(Issue.error(where, "Blocks in their listed order don't pass the tests: " + summarise(report)));
        }
    }

    private void validatePredict(Exercise exercise, String where, List<Issue> issues) {
        String mainFile = exercise.entry().mainFile();
        if (!exercise.starter().containsKey(mainFile)) {
            issues.add(Issue.error(where, "Predict exercise needs starter/" + mainFile));
            return;
        }
        if (exercise.spec().expectedOutput() == null) {
            issues.add(Issue.error(where, "Predict exercise needs expected_output"));
            return;
        }
        GradeReport report = grader.grade(exercise, new Submission(null, exercise.spec().expectedOutput(), null, null));
        if (!report.passed()) {
            issues.add(Issue.error(where, "expected_output doesn't match the real output, which is:\n" + report.actualOutput()));
        }
    }

    private void validateExplain(Exercise exercise, Content content, String where, List<Issue> issues) {
        Exercise.Rubric rubric = exercise.spec().rubric();
        if (rubric == null || rubric.levels() == null) {
            issues.add(Issue.error(where, "Explain exercise needs a rubric"));
            return;
        }
        Set<Integer> scores = new HashSet<>();
        for (Exercise.RubricLevel level : rubric.levels()) {
            scores.add(level.score());
            if (orEmpty(level.samples()).size() < 2) {
                issues.add(Issue.error(where, "Rubric level " + level.score() + " needs at least 2 sample answers"));
            }
        }
        if (!scores.equals(Set.of(0, 1, 2))) {
            issues.add(Issue.error(where, "Rubric needs exactly the levels 0, 1 and 2"));
        }
        String refersTo = exercise.spec().refersTo();
        if (refersTo != null && content.exercise(refersTo).isEmpty()) {
            issues.add(Issue.error(where, "refers_to unknown exercise " + refersTo));
        }
    }

    /** Checks the test definitions themselves; returns false if they are too broken to run. */
    private boolean checkTests(Exercise exercise, String where, List<Issue> issues) {
        Exercise.Spec spec = exercise.spec();
        if (spec.tests() == null || exercise.allTests().findAny().isEmpty()) {
            issues.add(Issue.error(where, "Has no tests"));
            return false;
        }
        boolean ok = true;
        for (MethodSpec method : exercise.entry().methodsOrEmpty()) {
            List<String> types = new ArrayList<>(orEmpty(method.params()).stream().map(Exercise.Param::type).toList());
            types.add(method.returns());
            for (String type : types) {
                if (type == null || !academy.assessment.JavaLiterals.isSupported(type)) {
                    issues.add(Issue.error(where, "Method " + method.name() + " uses unsupported test type " + type));
                    ok = false;
                }
            }
        }
        for (var test : exercise.allTests().toList()) {
            int kinds = (test.test().isMethodTest() ? 1 : 0) + (test.test().isIoTest() ? 1 : 0) + (test.test().isSourceTest() ? 1 : 0);
            if (kinds != 1) {
                issues.add(Issue.error(where, "Each test must be exactly one of: a method test (args/expect), an I/O test (stdin/stdout_*), or a source test (source_contains/source_not_contains)"));
                ok = false;
            }
            if (test.test().isIoTest() && test.test().stdoutEquals() == null && test.test().stdoutContains() == null) {
                issues.add(Issue.error(where, "I/O test needs stdout_equals or stdout_contains"));
                ok = false;
            }
        }
        return ok;
    }

    private GradeReport grade(Exercise exercise, Map<String, String> files, String where, List<Issue> issues) {
        try {
            return grader.grade(exercise, Submission.ofFiles(files));
        } catch (IllegalArgumentException | IllegalStateException e) {
            issues.add(Issue.error(where, "Could not grade: " + e.getMessage()));
            return null;
        }
    }

    private void validateVariantGroups(Content content, List<Issue> issues) {
        Map<String, List<Exercise>> groups = new HashMap<>();
        for (Exercise exercise : content.exercises().values()) {
            if (exercise.spec().variantGroup() != null) {
                groups.computeIfAbsent(exercise.spec().variantGroup(), g -> new ArrayList<>()).add(exercise);
            }
        }
        groups.forEach((group, members) -> {
            if (members.size() < MIN_VARIANT_GROUP_SIZE) {
                LessonStatus strictest = members.stream()
                        .map(e -> content.lesson(e.spec().lesson()).map(Lesson::status).orElse(LessonStatus.DRAFT))
                        .filter(LessonStatus::heldToPublicationStandard).findAny().orElse(LessonStatus.DRAFT);
                issues.add(new Issue(standardSeverity(strictest), "variant group " + group,
                        "Has " + members.size() + " exercise(s); retrieval needs the original plus at least 2 variants"));
            }
        });
    }

    private static void checkPlaceholders(String text, String where, Issue.Severity severity, List<Issue> issues) {
        Matcher m = PLACEHOLDER.matcher(text);
        if (m.find()) {
            issues.add(new Issue(severity, where, "Contains placeholder text '" + m.group() + "'"));
        }
    }

    private static Issue.Severity standardSeverity(LessonStatus status) {
        return status.heldToPublicationStandard() ? Issue.Severity.ERROR : Issue.Severity.WARNING;
    }

    private static void requireText(String value, String field, String where, List<Issue> issues) {
        if (value == null || value.isBlank()) {
            issues.add(Issue.error(where, "Missing " + field));
        }
    }

    private static String summarise(GradeReport report) {
        if (report.outcome() == GradeReport.Outcome.COMPILE_ERROR) {
            return "compile errors " + report.diagnostics();
        }
        return report.tests().stream().filter(t -> !t.passed())
                .map(t -> t.call() + " → " + t.status() + (t.actual() == null ? "" : " (got " + t.actual() + ", expected " + t.expected() + ")")
                        + (t.error() == null ? "" : " " + t.error()))
                .collect(Collectors.joining("; "));
    }

    private static <T> List<T> orEmpty(List<T> list) {
        return list == null ? List.of() : list;
    }
}
