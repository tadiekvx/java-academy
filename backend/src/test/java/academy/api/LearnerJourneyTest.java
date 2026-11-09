package academy.api;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Instant;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.time.temporal.ChronoUnit;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.jdbc.core.simple.JdbcClient;

/** Registration, onboarding, attempts and progress, end to end against the test database. */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class LearnerJourneyTest {

    private static final String CORRECT_AVERAGE = """
            {"files": {"Main.java": "double average(int a, int b) {\\n    return (a + b) / 2.0;\\n}\\nvoid main() {\\n}\\n"}}
            """;

    @LocalServerPort
    int port;

    @Autowired
    JdbcClient jdbc;

    @Test
    void registersOnboardsAndLogsBackIn() throws Exception {
        ApiClient client = new ApiClient(port);
        String email = "Ada-" + UUID.randomUUID() + "@Example.test";

        var registered = client.post("/api/auth/register",
                "{\"email\":\"" + email + "\",\"displayName\":\"Ada\",\"password\":\"correct horse battery\"}");
        assertThat(registered.statusCode()).isEqualTo(200);
        assertThat(registered.body()).contains("\"email\":\"" + email.toLowerCase() + "\"").contains("\"onboarded\":false");

        var onboarded = client.post("/api/onboarding", "{\"experience\":\"none\",\"weeklyHours\":5,\"goal\":\"career-change\"}");
        assertThat(onboarded.body()).contains("\"onboarded\":true");

        assertThat(client.post("/api/auth/logout", "").statusCode()).isEqualTo(204);
        assertThat(client.get("/api/auth/me").body()).isEqualTo("{\"learner\":null}");

        ApiClient again = new ApiClient(port);
        assertThat(again.post("/api/auth/login", "{\"email\":\"" + email + "\",\"password\":\"wrong password!\"}").statusCode())
                .isEqualTo(401);
        var loggedIn = again.post("/api/auth/login", "{\"email\":\"" + email + "\",\"password\":\"correct horse battery\"}");
        assertThat(loggedIn.statusCode()).isEqualTo(200);
        assertThat(loggedIn.body()).contains("\"displayName\":\"Ada\"").contains("\"onboarded\":true");
    }

    @Test
    void rejectsInvalidRegistrations() throws Exception {
        ApiClient client = new ApiClient(port);

        var shortPassword = client.post("/api/auth/register",
                "{\"email\":\"someone@example.test\",\"displayName\":\"Sam\",\"password\":\"short\"}");
        var badEmail = client.post("/api/auth/register",
                "{\"email\":\"not-an-email\",\"displayName\":\"Sam\",\"password\":\"long enough password\"}");

        assertThat(shortPassword.statusCode()).isEqualTo(400);
        assertThat(shortPassword.body()).contains("at least 10 characters");
        assertThat(badEmail.statusCode()).isEqualTo(400);
    }

    @Test
    void rejectsADuplicateEmail() throws Exception {
        String email = "dup-" + UUID.randomUUID() + "@example.test";
        String body = "{\"email\":\"" + email + "\",\"displayName\":\"Sam\",\"password\":\"long enough password\"}";

        new ApiClient(port).post("/api/auth/register", body);
        var second = new ApiClient(port).post("/api/auth/register", body);

        assertThat(second.statusCode()).isEqualTo(409);
    }

    @Test
    void attemptsAndVisitsShowUpAsProgress() throws Exception {
        ApiClient client = new ApiClient(port).registerNewLearner();

        client.post("/api/lessons/j1-l2.3/visit", "");
        assertThat(conceptJson(client, "J1.02")).contains("\"levelName\":\"Introduced\"");

        client.post("/api/exercises/j1-l2.3-write-average/attempts", CORRECT_AVERAGE);
        String concept = conceptJson(client, "J1.02");
        assertThat(concept).contains("\"levelName\":\"Practising\"").contains("\"independentExercises\":1");
        assertThat(concept).contains("{\"type\":\"IMPL\",\"label\":\"Write it yourself\",\"coverage\":\"INDEPENDENT\"}");

        String lesson = client.get("/api/progress/lessons/j1-l2.3").body();
        assertThat(lesson).contains("\"j1-l2.3-write-average\":{\"attempts\":1,\"passed\":true,\"passedIndependently\":true");

        String progress = client.get("/api/progress").body();
        assertThat(progress).contains("\"recommended\":{\"id\":\"j1-l1.1\"").contains("\"dueChecks\":[]");
    }

    @Test
    void remembersWhatTheLearnerSubmittedAndTracksLessonProgress() throws Exception {
        ApiClient client = new ApiClient(port).registerNewLearner();

        assertThat(client.get("/api/progress/lessons").body()).isEqualTo("{}");

        client.post("/api/lessons/j1-l2.3/visit", "");
        assertThat(client.get("/api/progress/lessons").body())
                .contains("\"j1-l2.3\":{\"visited\":true").contains("\"attempted\":0").contains("\"completed\":false");

        client.post("/api/exercises/j1-l2.3-predict-precedence/attempts", "{\"prediction\":\"14\\n20\\n2\\n3\"}");
        client.post("/api/exercises/j1-l2.3-write-average/attempts", CORRECT_AVERAGE);

        // The last input comes back with the result the learner was shown.
        String lesson = client.get("/api/progress/lessons/j1-l2.3").body();
        assertThat(lesson).contains("\"prediction\":\"14\\n20\\n2\\n3\"").contains("\"actualOutput\":");
        assertThat(lesson).contains("double average(int a, int b)");

        assertThat(client.get("/api/progress/lessons").body()).contains("\"attempted\":2");

        assertThat(client.post("/api/lessons/j1-l2.3/complete", "").statusCode()).isEqualTo(200);
        assertThat(client.get("/api/progress/lessons").body()).contains("\"completed\":true");
        assertThat(client.delete("/api/lessons/j1-l2.3/complete").statusCode()).isEqualTo(200);
        assertThat(client.get("/api/progress/lessons").body()).contains("\"completed\":false");
    }

    @Test
    void onlyTheFirstPredictionCountsAsIndependent() throws Exception {
        ApiClient client = new ApiClient(port).registerNewLearner();
        String exercise = "/api/exercises/j1-l2.3-predict-precedence/attempts";

        client.post(exercise, "{\"prediction\":\"14\\n20\\n2\\n3\"}");
        client.post(exercise, "{\"prediction\":\"14\\n20\\n50\\n3\"}");

        assertThat(client.get("/api/progress/lessons/j1-l2.3").body())
                .contains("\"j1-l2.3-predict-precedence\":{\"attempts\":2,\"passed\":true,\"passedIndependently\":false");
    }

    @Test
    void offersAKnowledgeCheckOnceItIsDueAndAcceptsItOnlyThen() throws Exception {
        ApiClient client = new ApiClient(port).registerNewLearner();
        long learnerId = learnerId(client);

        assertThat(client.post("/api/exercises/j1-l2.3-retrieve-price-per-item/attempts?context=retrieval",
                "{\"files\":{\"Main.java\":\"void main() {}\"}}").statusCode()).isEqualTo(400);

        // Four days ago the learner showed every kind of evidence J1.02 needs, independently. The explanation
        // is recorded as reviewed and passed, which the review workflow will do once it exists.
        Instant fourDaysAgo = Instant.now().minus(4, ChronoUnit.DAYS);
        insertPassedAttempt(learnerId, "j1-l2.3-write-average", fourDaysAgo);
        insertPassedAttempt(learnerId, "j1-l2.3-predict-division", fourDaysAgo);
        insertPassedAttempt(learnerId, "j1-l2.3-explain-rounding-up", fourDaysAgo);

        String progress = client.get("/api/progress").body();
        assertThat(conceptJson(client, "J1.02")).contains("\"levelName\":\"Demonstrated\"");
        Matcher due = Pattern.compile("\"dueChecks\":\\[\\{\"exerciseId\":\"([^\"]+)\"").matcher(progress);
        assertThat(due.find()).as(progress).isTrue();
        String checkExercise = due.group(1);
        assertThat(checkExercise).matches("j1-l2\\.\\d-retrieve-.+");

        var attempt = client.post("/api/exercises/" + checkExercise + "/attempts?context=retrieval",
                "{\"files\":{\"Main.java\":\"void main() {}\"}}");
        assertThat(attempt.statusCode()).isEqualTo(200);

        // The check failed (the code doesn't even declare the method), so the schedule restarts and nothing is due.
        assertThat(client.get("/api/progress").body()).contains("\"dueChecks\":[]");
        assertThat(conceptJson(client, "J1.02")).contains("\"levelName\":\"Demonstrated\"");
    }

    private long learnerId(ApiClient client) throws Exception {
        Matcher m = Pattern.compile("\"id\":(\\d+)").matcher(client.get("/api/auth/me").body());
        assertThat(m.find()).isTrue();
        return Long.parseLong(m.group(1));
    }

    private void insertPassedAttempt(long learnerId, String exerciseId, Instant at) {
        jdbc.sql("""
                        insert into attempt (learner_id, exercise_id, submitted_at, context, outcome, tests_passed, tests_total, submission)
                        values (:learnerId, :exerciseId, :at, 'practice', 'PASSED', 1, 1, '{}')""")
                .param("learnerId", learnerId)
                .param("exerciseId", exerciseId)
                .param("at", OffsetDateTime.ofInstant(at, ZoneOffset.UTC))
                .update();
    }

    /** The JSON object for one concept in the learner's progress. */
    private static String conceptJson(ApiClient client, String conceptId) throws Exception {
        String body = client.get("/api/progress").body();
        int start = body.indexOf("{\"id\":\"" + conceptId + "\"");
        assertThat(start).as(body).isGreaterThanOrEqualTo(0);
        int end = body.indexOf("\"nextCheckDue\"", start);
        return body.substring(start, body.indexOf('}', end) + 1);
    }
}
