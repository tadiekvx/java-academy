package academy.mentor;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonPropertyDescription;

/**
 * The language model behind the mentor. {@link ClaudeMentorModel} is the real one; tests use a
 * scripted fake. Implementations only generate text: every policy decision is made by
 * {@link MentorService} before and after the call.
 */
public interface MentorModel {

    boolean available();

    /** Identifies the model in logs and stored records, e.g. {@code claude-opus-5-5}. */
    String id();

    /**
     * @throws MentorUnavailableException if the model can't be reached or declines to answer
     */
    MentorReply reply(String context, List<Turn> history, String request);

    /**
     * @throws MentorUnavailableException if the model can't be reached or declines to answer
     */
    RubricScore score(String rubricPrompt);

    /** A previous message in this exercise's conversation. */
    record Turn(boolean fromLearner, String text) {}

    /** The mentor's structured reply. */
    record MentorReply(
            @JsonPropertyDescription("What the learner sees. Markdown. Must not contain fenced code blocks; put code in the code field.")
            String message,
            @JsonPropertyDescription("A complete Java 25 compact source file (with void main()) to show the learner, or an empty string. Only allowed at H3 and H4.")
            String code,
            @JsonPropertyDescription("Exactly what running the code prints, or an empty string when there is no code.")
            String codeExpectedOutput,
            @JsonPropertyDescription("True if the learner's latest message asks for the answer or full solution instead of help.")
            boolean solutionRequest) {}

    /** A score against a 0–2 rubric. */
    record RubricScore(
            @JsonPropertyDescription("0, 1 or 2, using the rubric's level descriptors and sample answers as anchors.")
            int score,
            @JsonPropertyDescription("One or two sentences for reviewers: why this score.")
            String rationale,
            @JsonPropertyDescription("Two or three sentences to the learner: what was good, and what a full answer would add.")
            String feedback) {}
}
