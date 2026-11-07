package academy.api;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.stream.IntStream;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import academy.assessment.GradeReport;
import academy.assessment.Grader;
import academy.assessment.Submission;
import academy.assessment.TestDescriptions;
import academy.content.Exercise;
import academy.content.ExerciseType;
import academy.learner.CurrentLearner;
import academy.mentor.MentorService;
import academy.progress.AttemptContext;
import academy.progress.ProgressService;

@RestController
@RequestMapping("/api")
class ExerciseController {

    private final ContentAccess access;
    private final Grader grader;
    private final ProgressService progress;
    private final MentorService mentor;

    ExerciseController(ContentAccess access, Grader grader, ProgressService progress, MentorService mentor) {
        this.access = access;
        this.grader = grader;
        this.progress = progress;
        this.mentor = mentor;
    }

    /** What a learner sees of an exercise: never the solution, hidden tests or expected output. */
    record ExerciseView(
            String id,
            ExerciseType type,
            String title,
            String prompt,
            Map<String, String> files,
            List<String> signatures,
            List<TestView> visibleTests,
            List<Block> blocks,
            String relatedCode) {}

    record TestView(String name, String call, String expected) {}

    record Block(int index, String text) {}

    record RunRequest(Map<String, String> files, String stdin) {}

    @GetMapping("/exercises/{id}")
    ExerciseView exercise(@PathVariable String id) {
        Exercise exercise = access.exercise(id);
        var spec = exercise.spec();
        List<TestView> visible = spec.tests() == null ? List.of() : spec.tests().visibleOrEmpty().stream()
                .map(t -> new TestView(t.name(), TestDescriptions.call(exercise, t), TestDescriptions.expected(t)))
                .toList();
        String relatedCode = spec.refersTo() == null ? null : access.content().exercise(spec.refersTo())
                .map(related -> related.starter().get(related.entry().mainFile())).orElse(null);
        return new ExerciseView(exercise.id(), exercise.type(), spec.title(), spec.prompt(),
                spec.type() == ExerciseType.PARSONS ? Map.of() : exercise.starter(),
                exercise.entry().methodsOrEmpty().stream().map(Exercise.MethodSpec::signature).toList(),
                visible, shuffledBlocks(exercise), relatedCode);
    }

    /** Grades and records an attempt. {@code context=retrieval} is only accepted for a due knowledge check. */
    @PostMapping("/exercises/{id}/attempts")
    GradeReport attempt(@PathVariable String id, @RequestBody Submission submission,
            @RequestParam(defaultValue = "practice") String context, Authentication authentication) {
        long learnerId = CurrentLearner.require(authentication);
        Exercise exercise = access.exercise(id);
        AttemptContext attemptContext = switch (context) {
            case "practice" -> AttemptContext.PRACTICE;
            case "retrieval" -> AttemptContext.RETRIEVAL;
            default -> throw new IllegalArgumentException("Unknown attempt context " + context);
        };
        if (attemptContext == AttemptContext.RETRIEVAL) {
            progress.requireDueCheck(learnerId, id);
        }
        GradeReport report = grader.grade(exercise, submission);
        MentorService.Assistance assistance = mentor.assistance(learnerId, id);
        long attemptId = progress.recordAttempt(learnerId, exercise, submission, report, attemptContext,
                assistance.level(), assistance.solutionViewed());
        if (exercise.type() == ExerciseType.EXPLAIN) {
            report = mentor.scoreExplanation(attemptId, exercise, submission.explanation())
                    .map(score -> new GradeReport(score.score() == 2 ? GradeReport.Outcome.PASSED : GradeReport.Outcome.FAILED,
                            "Provisional score " + score.score() + "/2 (scored by the AI mentor; a reviewer may adjust it). "
                                    + score.feedback(), List.of(), List.of(), null))
                    .orElse(report);
        }
        return report.forLearner();
    }

    @PostMapping("/run")
    Grader.ProgramRun run(@RequestBody RunRequest request) {
        return grader.runProgram(request.files(), "Main", request.stdin() == null ? "" : request.stdin());
    }

    /** Parsons blocks in a stable shuffled order (seeded by exercise id), keeping their palette indices. */
    private static List<Block> shuffledBlocks(Exercise exercise) {
        if (exercise.type() != ExerciseType.PARSONS) {
            return List.of();
        }
        List<String> palette = exercise.parsonsPalette();
        List<Block> blocks = new ArrayList<>(IntStream.range(0, palette.size()).mapToObj(i -> new Block(i, palette.get(i))).toList());
        Collections.shuffle(blocks, new Random(exercise.id().hashCode()));
        return blocks;
    }
}
