package academy.mentor;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;

import org.junit.jupiter.api.Test;

import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaOutputConfig;

/** Checks the requests the mentor builds, without calling the API. */
class ClaudeMentorModelTest {

    private final ClaudeMentorModel model = new ClaudeMentorModel(new MentorProperties("claude-opus-5-5", 60));

    @Test
    void replyRequestsUseStructuredOutputMediumEffortAndRefusalFallbacks() {
        var params = model.replyParams("EXERCISE: …", List.of(new MentorModel.Turn(true, "hi"), new MentorModel.Turn(false, "hello")),
                "GRANTED HELP LEVEL: H1 Nudge");
        var raw = params.rawParams();

        assertThat(raw.model().asString()).isEqualTo("claude-opus-5-5");
        assertThat(raw.betas()).hasValueSatisfying(b -> assertThat(b).contains(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01));
        assertThat(raw.fallbacks()).isPresent();
        assertThat(raw.outputConfig()).hasValueSatisfying(c -> assertThat(c.effort()).contains(BetaOutputConfig.Effort.MEDIUM));
        assertThat(raw.outputConfig().orElseThrow().toString()).contains("solutionRequest").contains("codeExpectedOutput");
        assertThat(raw.system().orElseThrow().toString()).contains("cacheControl=BetaCacheControlEphemeral").contains("H4 Walkthrough");
    }

    @Test
    void conversationTurnsAlternateStartingAfterTheExerciseContext() {
        var raw = model.replyParams("EXERCISE", List.of(new MentorModel.Turn(true, "q1"), new MentorModel.Turn(false, "a1")), "q2").rawParams();

        assertThat(raw.messages()).extracting(m -> m.role().asString()).containsExactly("user", "assistant", "user", "assistant", "user");
    }

    @Test
    void scoreRequestsAskForARubricScore() {
        var raw = model.scoreParams("RUBRIC …").rawParams();

        assertThat(raw.outputConfig().orElseThrow().toString()).contains("score").contains("rationale").contains("feedback");
    }

    @Test
    void isUnavailableWithoutCredentials() {
        if (System.getenv("ANTHROPIC_API_KEY") == null && System.getenv("ANTHROPIC_AUTH_TOKEN") == null) {
            assertThat(model.available()).isFalse();
        }
    }
}
