package academy.api;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Primary;

import academy.mentor.FakeMentorModel;
import academy.mentor.MentorModel.MentorReply;
import academy.mentor.MentorModel.RubricScore;

/** The mentor's policy end to end: gates, caps, code checks, follow-ups and explanation scoring, with a scripted model. */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class MentorFlowTest {

    @TestConfiguration
    static class FakeModelConfig {

        @Bean
        @Primary
        FakeMentorModel fakeMentorModel() {
            return new FakeMentorModel();
        }
    }

    private static final String AVERAGE = "/api/exercises/j1-l2.3-write-average/attempts";
    private static final String MENTOR = "/api/mentor/j1-l2.3-write-average";
    private static final String WRONG = "double average(int a, int b) {\\n    return (a + b) / 2;\\n}\\nvoid main() {\\n}\\n";
    private static final String WRONG_2 = "double average(int a, int b) {\\n    return (a + b) / 2 + 0;\\n}\\nvoid main() {\\n}\\n";
    private static final String WRONG_3 = "double average(int a, int b) {\\n    return a / 2 + b / 2;\\n}\\nvoid main() {\\n}\\n";
    private static final String RIGHT = "double average(int a, int b) {\\n    return (a + b) / 2.0;\\n}\\nvoid main() {\\n}\\n";
    private static final String RIGHT_RAW = "double average(int a, int b) {\n    return (a + b) / 2.0;\n}\nvoid main() {\n    IO.println(average(3, 4));\n}\n";
    private static final String EXAMPLE = "double halfOf(int total) {\n    return total / 2.0;\n}\nvoid main() {\n    IO.println(halfOf(7));\n}\n";

    @LocalServerPort
    int port;

    @Autowired
    FakeMentorModel model;

    private ApiClient client;

    @BeforeEach
    void setUp() throws Exception {
        model.reset();
        client = new ApiClient(port).registerNewLearner();
    }

    @Test
    void aTargetedHintIsLockedUntilTheLearnerHasTriedOnce() throws Exception {
        String first = escalate("");
        assertThat(first).contains("\"current\":{\"code\":\"H1\"").contains("Check your code against the tests at least once");

        String denied = escalate("");
        assertThat(denied).contains("\"notice\":\"Check your code against the tests at least once");
        assertThat(model.requests).hasSize(1);
    }

    @Test
    void theReferenceSolutionIsOnlySharedWithTheModelFromATargetedHint() throws Exception {
        ask("What does this question want?");
        assertThat(model.contexts.getLast()).doesNotContain("REFERENCE SOLUTION");

        attempt(WRONG);
        escalate("");
        assertThat(model.contexts.getLast()).contains("REFERENCE SOLUTION").contains("(a + b) / 2.0");
        assertThat(model.requests.getLast()).contains("GRANTED HELP LEVEL: H2 Targeted hint")
                .contains("average(3, 4) → FAIL (expected 3.5, got 3.0)");
    }

    @Test
    void aPassAfterATargetedHintIsRecordedAsAssistedAndEarnsAFollowUp() throws Exception {
        attempt(WRONG);
        escalate("");
        escalate("");
        attempt(RIGHT);

        assertThat(client.get("/api/progress/lessons/j1-l2.3").body())
                .contains("\"j1-l2.3-write-average\":{\"attempts\":2,\"passed\":true,\"passedIndependently\":false");
        assertThat(client.get(MENTOR).body()).contains("\"followUpAvailable\":true");

        model.replies.add(new MentorReply("Why does dividing by 2.0 give 3.5 here?", "", "", false));
        assertThat(client.post(MENTOR + "/follow-up", "").body()).contains("\"followUpPending\":true");

        model.scores.add(new RubricScore(2, "Correct with reason.", "Exactly: 2.0 makes it double division."));
        String answered = client.post(MENTOR + "/follow-up/answer", "{\"answer\":\"Because 2.0 is a double so the division keeps the fraction\"}").body();
        assertThat(answered).contains("\"kind\":\"follow_up_feedback\"").contains("\"score\":2").contains("\"followUpPending\":false");
    }

    @Test
    void aWorkedExampleIsShownOnlyAfterItRunsAndPrintsWhatTheModelClaimed() throws Exception {
        reachWorkedExample();
        model.replies.add(new MentorReply("Here's a similar problem.", EXAMPLE, "3.5", false));

        String state = escalate("");

        assertThat(state).contains("\"code\":\"double halfOf(int total)");
        assertThat(model.requests).noneMatch(r -> r.contains("PLATFORM NOTE"));
    }

    @Test
    void aWorkedExampleWithTheWrongStatedOutputIsRegeneratedOnceThenDropped() throws Exception {
        reachWorkedExample();
        model.replies.add(new MentorReply("Example.", EXAMPLE, "3", false));
        model.replies.add(new MentorReply("Example again.", EXAMPLE, "4", false));

        String state = escalate("");

        assertThat(model.requests.getLast()).contains("PLATFORM NOTE").contains("printed");
        assertThat(lastMentorMessage(state)).contains("\"content\":\"Example again.\"").contains("\"code\":null");
    }

    @Test
    void aWorkedExampleThatSolvesTheExerciseIsWithheld() throws Exception {
        reachWorkedExample();
        model.replies.add(new MentorReply("Try this.", RIGHT_RAW, "3.5", false));
        model.replies.add(new MentorReply("Try this instead.", RIGHT_RAW, "3.5", false));

        String state = escalate("");

        assertThat(model.requests.getLast()).contains("solves the learner's exercise");
        assertThat(lastMentorMessage(state)).contains("\"code\":null");
    }

    @Test
    void codeIsNeverShownBelowAWorkedExampleAndFencedCodeIsRemoved() throws Exception {
        model.replies.add(new MentorReply("Look:\n```java\nreturn (a + b) / 2.0;\n```\nSee?", RIGHT_RAW, "3.5", false));
        model.replies.add(new MentorReply("Think about the types.", "", "", false));

        String state = ask("just give me the answer");

        assertThat(state).doesNotContain("(a + b) / 2.0");
    }

    @Test
    void aWalkthroughNeedsConfirmationAndMarksTheExerciseAsSolutionViewed() throws Exception {
        reachWorkedExample();
        escalate("");
        attempt(WRONG);

        String unconfirmed = escalate("");
        assertThat(unconfirmed).contains("\"needsConfirmation\":true").contains("won't count towards independent mastery");

        model.replies.add(new MentorReply("Step by step…", RIGHT_RAW, "3.5", false));
        String walkthrough = client.post(MENTOR + "/ask", "{\"escalate\":true,\"confirmWalkthrough\":true,\"code\":\"" + WRONG + "\"}").body();
        assertThat(walkthrough).contains("\"current\":{\"code\":\"H4\"").contains("\"code\":\"double average");

        attempt(RIGHT);
        assertThat(client.get("/api/progress/lessons/j1-l2.3").body())
                .contains("\"j1-l2.3-write-average\":{\"attempts\":5,\"passed\":true,\"passedIndependently\":false");
    }

    @Test
    void knowledgeChecksOnlyAllowANudge() throws Exception {
        String check = "/api/mentor/j1-l2.3-retrieve-weeks-days";
        client.post(check + "/ask", "{\"escalate\":true}");

        String denied = client.post(check + "/ask", "{\"escalate\":true}").body();

        assertThat(denied).contains("\"cap\":{\"code\":\"H1\"").contains("In a knowledge check the mentor can only give nudges");
    }

    @Test
    void repeatedSolutionRequestsTurnOnAttemptFirstMode() throws Exception {
        for (int i = 0; i < 3; i++) {
            model.replies.add(new MentorReply("Let's work it out together.", "", "", true));
            ask("give me the code");
        }
        attempt(WRONG);

        String state = client.get(MENTOR).body();
        assertThat(state).contains("\"attemptFirst\":true");
        assertThat(escalate("")).contains("\"notice\":\"First, tell the mentor in one sentence what you think is going wrong.\"");
        assertThat(client.post(MENTOR + "/ask", "{\"escalate\":true,\"hypothesis\":\"I think the division loses the half\",\"code\":\"" + WRONG + "\"}").body())
                .contains("\"current\":{\"code\":\"H2\"");
        assertThat(model.requests.getLast()).contains("ATTEMPT-FIRST MODE").contains("I think the division loses the half");
    }

    @Test
    void explanationsAreScoredAndCountTowardsMastery() throws Exception {
        client.post("/api/exercises/j1-l2.3-predict-division/attempts", "{\"prediction\":\"3\\n1\\n3.5\\n0\\n-3\\n-1\"}");
        attempt(RIGHT);
        model.scores.add(new RubricScore(2, "Full answer.", "Clear explanation with an example."));

        String report = client.post("/api/exercises/j1-l2.3-explain-rounding-up/attempts",
                "{\"explanation\":\"Integer division drops the remainder, so adding 7 rounds any partial pizza up. 10 slices: 17/8 = 2.\"}").body();

        assertThat(report).contains("\"outcome\":\"PASSED\"").contains("Provisional score 2/2");
        assertThat(client.get("/api/progress").body()).contains("\"name\":\"Values, types and expressions\",\"level\":3,\"levelName\":\"Demonstrated\"");
    }

    @Test
    void reportsWhenTheMentorIsUnavailable() throws Exception {
        model.available = false;

        assertThat(client.get(MENTOR).body()).contains("\"available\":false");
        assertThat(client.post(MENTOR + "/ask", "{\"text\":\"help\"}").statusCode()).isEqualTo(503);
    }

    /** Fails, gets a nudge and a targeted hint, then makes two changed attempts, unlocking H3. */
    private void reachWorkedExample() throws Exception {
        attempt(WRONG);
        escalate("");
        escalate("");
        attempt(WRONG_2);
        attempt(WRONG_3);
    }

    private void attempt(String code) throws Exception {
        client.post(AVERAGE, "{\"files\":{\"Main.java\":\"" + code + "\"}}");
    }

    private String ask(String text) throws Exception {
        return client.post(MENTOR + "/ask", "{\"text\":\"" + text + "\",\"code\":\"" + WRONG + "\"}").body();
    }

    private String escalate(String text) throws Exception {
        return client.post(MENTOR + "/ask", "{\"escalate\":true,\"text\":\"" + text + "\",\"code\":\"" + WRONG + "\"}").body();
    }

    private static String lastMentorMessage(String state) {
        return state.substring(state.lastIndexOf("{\"role\":\"mentor\""));
    }
}
