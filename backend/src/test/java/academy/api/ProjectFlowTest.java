package academy.api;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;

/** Projects end to end: listing, viewing without leaks, grading a milestone, and progress. */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ProjectFlowTest {

    private static final String SOLVED_M1 = "{\"files\":{\"Main.java\":\"int totalExpenses(int[] expenses) {\\n    int total = 0;\\n    for (int e : expenses) {\\n        total += e;\\n    }\\n    return total;\\n}\\nvoid main() {}\\n\"}}";
    private static final String STUB = "{\"files\":{\"Main.java\":\"int totalExpenses(int[] expenses) {\\n    return 0;\\n}\\nvoid main() {}\\n\"}}";

    @LocalServerPort
    int port;

    private ApiClient client;

    @BeforeEach
    void setUp() {
        client = new ApiClient(port);
    }

    @Test
    void listsAllProjectsWithTheirCategories() throws Exception {
        String body = client.get("/api/projects").body();

        assertThat(body)
                .contains("\"id\":\"j1-p1-finance\"").contains("\"category\":\"A\"")
                .contains("\"id\":\"j1-p2-receipt\"").contains("\"id\":\"j1-p3-brightbank\"")
                .contains("\"id\":\"j1-a1-inherited-gradebook\"").contains("\"category\":\"C\"");
    }

    @Test
    void neverSendsTheSolutionOrHiddenTests() throws Exception {
        String body = client.get("/api/projects/j1-p1-finance").body();

        assertThat(body).contains("\"title\":\"Add up the expenses\"").contains("\"visibleTests\"");
        assertThat(body).doesNotContain("total += expense").doesNotContain("one big expense").doesNotContain("solution");
    }

    @Test
    void gradesAMilestoneAndTracksProgress() throws Exception {
        client.registerNewLearner();

        var failed = client.post("/api/projects/j1-p1-finance/milestones/m1/attempts", STUB);
        assertThat(failed.statusCode()).isEqualTo(200);
        assertThat(failed.body()).contains("\"outcome\":\"FAILED\"").contains("\"call\":\"totalExpenses([5000])\"");

        var passed = client.post("/api/projects/j1-p1-finance/milestones/m1/attempts", SOLVED_M1);
        assertThat(passed.body()).contains("\"outcome\":\"PASSED\"");

        assertThat(client.get("/api/progress/projects/j1-p1-finance").body())
                .contains("\"m1\":{\"attempts\":2,\"passed\":true,\"passedIndependently\":true")
                .contains("\"m2\":{\"attempts\":0,\"passed\":false");
    }

    @Test
    void projectWorkCountsAsMasteryEvidence() throws Exception {
        client.registerNewLearner();
        client.post("/api/projects/j1-p1-finance/milestones/m1/attempts", SOLVED_M1);

        // A guided project (category A) gives IMPL evidence for the project's concepts.
        assertThat(client.get("/api/progress").body()).contains("\"name\":\"Arrays\",\"level\":2,\"levelName\":\"Practising\"");
    }

    @Test
    void attemptsNeedALoggedInLearner() throws Exception {
        assertThat(client.post("/api/projects/j1-p1-finance/milestones/m1/attempts", STUB).statusCode()).isEqualTo(401);
    }

    @Test
    void unknownProjectsAndMilestonesAreNotFound() throws Exception {
        client.registerNewLearner();

        assertThat(client.get("/api/projects/nope").statusCode()).isEqualTo(404);
        assertThat(client.post("/api/projects/j1-p1-finance/milestones/m99/attempts", STUB).statusCode()).isEqualTo(404);
    }
}
