package academy.mentor;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.errors.AnthropicException;
import com.anthropic.models.beta.AnthropicBeta;
import com.anthropic.models.beta.messages.BetaCacheControlEphemeral;
import com.anthropic.models.beta.messages.BetaFallbacksParam;
import com.anthropic.models.beta.messages.BetaOutputConfig;
import com.anthropic.models.beta.messages.BetaStopReason;
import com.anthropic.models.beta.messages.BetaTextBlockParam;
import com.anthropic.models.beta.messages.MessageCreateParams;
import com.anthropic.models.beta.messages.StructuredMessage;
import com.anthropic.models.beta.messages.StructuredMessageCreateParams;

/**
 * The mentor on Claude, via the official Java SDK. Replies use structured output so the service
 * can validate code before anyone sees it. Requests opt in to server-side refusal fallbacks, so a
 * safety-classifier refusal is retried on a fallback model instead of failing the learner's request.
 */
@Component
public class ClaudeMentorModel implements MentorModel {

    private static final Logger log = LoggerFactory.getLogger(ClaudeMentorModel.class);
    private static final long MAX_TOKENS = 16000L;

    private final MentorProperties properties;
    private final AnthropicClient client;

    public ClaudeMentorModel(MentorProperties properties) {
        this.properties = properties;
        this.client = hasCredentials() ? AnthropicOkHttpClient.fromEnv() : null;
        if (client == null) {
            log.warn("No ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN set: the AI mentor is unavailable");
        }
    }

    @Override
    public boolean available() {
        return client != null;
    }

    @Override
    public String id() {
        return properties.model();
    }

    @Override
    public MentorReply reply(String context, List<Turn> history, String request) {
        return call(replyParams(context, history, request));
    }

    @Override
    public RubricScore score(String rubricPrompt) {
        return call(scoreParams(rubricPrompt));
    }

    StructuredMessageCreateParams<MentorReply> replyParams(String context, List<Turn> history, String request) {
        MessageCreateParams.Builder builder = baseParams(MentorPrompts.MENTOR_SYSTEM);
        builder.addUserMessage(context);
        if (history.isEmpty() || history.getFirst().fromLearner()) {
            // Messages must alternate; the context is a user turn, so the history must open with the mentor.
            builder.addAssistantMessage("Understood. I'll keep to the granted help level.");
        }
        for (Turn turn : history) {
            if (turn.fromLearner()) {
                builder.addUserMessage(turn.text());
            } else {
                builder.addAssistantMessage(turn.text());
            }
        }
        builder.addUserMessage(request);
        return builder.outputConfig(MentorReply.class, BetaOutputConfig.Effort.MEDIUM).build();
    }

    StructuredMessageCreateParams<RubricScore> scoreParams(String rubricPrompt) {
        MessageCreateParams.Builder builder = baseParams(MentorPrompts.SCORER_SYSTEM);
        builder.addUserMessage(rubricPrompt);
        return builder.outputConfig(RubricScore.class, BetaOutputConfig.Effort.MEDIUM).build();
    }

    private MessageCreateParams.Builder baseParams(String system) {
        return MessageCreateParams.builder()
                .model(properties.model())
                .maxTokens(MAX_TOKENS)
                .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01)
                .fallbacks(BetaFallbacksParam.ofDefault())
                .systemOfBetaTextBlockParams(List.of(BetaTextBlockParam.builder()
                        .text(system)
                        .cacheControl(BetaCacheControlEphemeral.builder().build())
                        .build()));
    }

    private <T> T call(StructuredMessageCreateParams<T> params) {
        if (client == null) {
            throw new MentorUnavailableException("The mentor isn't configured on this server.");
        }
        StructuredMessage<T> message;
        try {
            message = client.beta().messages().create(params);
        } catch (AnthropicException e) {
            log.warn("Mentor model call failed", e);
            throw new MentorUnavailableException("The mentor couldn't be reached. Try again in a moment.", e);
        }
        BetaStopReason stop = message.stopReason().orElse(null);
        if (BetaStopReason.REFUSAL.equals(stop) || BetaStopReason.MAX_TOKENS.equals(stop)) {
            log.warn("Mentor model stopped with {}", stop);
            throw new MentorUnavailableException("The mentor couldn't answer that one. Try rephrasing your question.");
        }
        return message.content().stream()
                .flatMap(block -> block.text().stream())
                .map(text -> text.text())
                .findFirst()
                .orElseThrow(() -> new MentorUnavailableException("The mentor gave an empty answer. Try again."));
    }

    private static boolean hasCredentials() {
        return notBlank(System.getenv("ANTHROPIC_API_KEY")) || notBlank(System.getenv("ANTHROPIC_AUTH_TOKEN"));
    }

    private static boolean notBlank(String value) {
        return value != null && !value.isBlank();
    }
}
