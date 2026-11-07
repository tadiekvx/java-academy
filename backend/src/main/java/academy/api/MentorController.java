package academy.api;

import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import academy.learner.CurrentLearner;
import academy.mentor.MentorService;
import academy.mentor.MentorService.MentorState;

@RestController
@RequestMapping("/api/mentor")
class MentorController {

    private final MentorService mentor;
    private final ContentAccess access;

    MentorController(MentorService mentor, ContentAccess access) {
        this.mentor = mentor;
        this.access = access;
    }

    record FollowUpAnswer(String answer) {}

    @GetMapping("/{exerciseId}")
    MentorState state(@PathVariable String exerciseId, Authentication authentication) {
        return mentor.state(CurrentLearner.require(authentication), access.exercise(exerciseId));
    }

    @PostMapping("/{exerciseId}/ask")
    MentorState ask(@PathVariable String exerciseId, @RequestBody MentorService.AskRequest request, Authentication authentication) {
        return mentor.ask(CurrentLearner.require(authentication), access.exercise(exerciseId), request);
    }

    @PostMapping("/{exerciseId}/follow-up")
    MentorState followUp(@PathVariable String exerciseId, Authentication authentication) {
        return mentor.followUpQuestion(CurrentLearner.require(authentication), access.exercise(exerciseId));
    }

    @PostMapping("/{exerciseId}/follow-up/answer")
    MentorState answer(@PathVariable String exerciseId, @RequestBody FollowUpAnswer body, Authentication authentication) {
        return mentor.answerFollowUp(CurrentLearner.require(authentication), access.exercise(exerciseId), body.answer());
    }
}
