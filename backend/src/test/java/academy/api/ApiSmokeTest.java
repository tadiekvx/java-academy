package academy.api;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

/** Starts the whole application against the repository content and calls the learner API. */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ApiSmokeTest {

    private static final String BUGGY_PERCENTAGE = """
            {"files": {"Main.java": "double percentage(int correct, int total) {\\n    return correct / total * 100;\\n}\\nvoid main() {\\n}\\n"}}
            """;

    @LocalServerPort
    int port;

    private ApiClient client;

    @BeforeEach
    void setUp() {
        client = new ApiClient(port);
    }

    @Test
    void listsTheWholeStageOneCurriculumWithEveryLessonAvailable() throws Exception {
        var response = client.get("/api/curriculum");

        assertThat(response.statusCode()).isEqualTo(200);
        assertThat(response.body())
                .contains("\"id\":\"j1-l1.1\",\"title\":\"Your first program\",\"available\":true")
                .contains("\"id\":\"j1-l2.3\",\"title\":\"Arithmetic: division, remainders and exact results\",\"available\":true")
                .contains("\"id\":\"j1-l6.5\",\"title\":\"Debugging systematically\",\"available\":true")
                .doesNotContain("\"available\":false");
    }

    @Test
    void neverSendsSolutionsHiddenTestsOrExpectedOutput() throws Exception {
        String debug = client.get("/api/exercises/j1-l2.3-debug-percentage").body();
        String predict = client.get("/api/exercises/j1-l2.3-predict-division").body();

        assertThat(debug).contains("correct / total * 100").doesNotContain("100.0 / total").doesNotContain("one third");
        assertThat(predict).doesNotContain("expected").doesNotContain("3.5\\n");
    }

    @Test
    void gradesAnAttemptAndRedactsHiddenTests() throws Exception {
        client.registerNewLearner();

        var response = client.post("/api/exercises/j1-l2.3-debug-percentage/attempts", BUGGY_PERCENTAGE);

        assertThat(response.statusCode()).isEqualTo(200);
        assertThat(response.body())
                .contains("\"outcome\":\"FAILED\"")
                .contains("\"call\":\"percentage(3, 4)\",\"expected\":\"75.0\",\"actual\":\"0.0\"")
                .contains("\"name\":\"one third\",\"visible\":false,\"status\":\"FAIL\",\"call\":null");
    }

    @Test
    void runningCodeAndSubmittingAttemptsNeedALoggedInLearner() throws Exception {
        assertThat(client.post("/api/exercises/j1-l2.3-debug-percentage/attempts", BUGGY_PERCENTAGE).statusCode()).isEqualTo(401);
        assertThat(client.post("/api/run", "{\"files\":{\"Main.java\":\"void main() {}\"}}").statusCode()).isEqualTo(401);
    }

    @Test
    void rejectsStateChangingRequestsWithoutTheCsrfToken() throws Exception {
        client.registerNewLearner();

        assertThat(client.postWithoutCsrf("/api/exercises/j1-l2.3-debug-percentage/attempts", BUGGY_PERCENTAGE).statusCode())
                .isEqualTo(403);
    }

    @Test
    void returnsNotFoundForUnknownExercises() throws Exception {
        assertThat(client.get("/api/exercises/no-such-exercise").statusCode()).isEqualTo(404);
    }
}
