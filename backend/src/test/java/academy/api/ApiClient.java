package academy.api;

import java.io.IOException;
import java.net.CookieManager;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.UUID;

/** A browser-like test client: keeps the session cookie and echoes the CSRF cookie as a header. */
class ApiClient {

    private final int port;
    private final CookieManager cookies = new CookieManager();
    private final HttpClient http;

    ApiClient(int port) {
        this.port = port;
        this.http = HttpClient.newBuilder().cookieHandler(cookies).build();
    }

    /** Registers a new learner with a unique email and logs in as them. */
    ApiClient registerNewLearner() throws Exception {
        String email = "learner-" + UUID.randomUUID() + "@example.test";
        HttpResponse<String> response = post("/api/auth/register",
                "{\"email\":\"" + email + "\",\"displayName\":\"Test Learner\",\"password\":\"correct horse battery\"}");
        if (response.statusCode() != 200) {
            throw new IllegalStateException("Registration failed: " + response.statusCode() + " " + response.body());
        }
        return this;
    }

    HttpResponse<String> get(String path) throws IOException, InterruptedException {
        return http.send(HttpRequest.newBuilder(uri(path)).build(), HttpResponse.BodyHandlers.ofString());
    }

    HttpResponse<String> post(String path, String json) throws IOException, InterruptedException {
        return http.send(HttpRequest.newBuilder(uri(path))
                        .header("Content-Type", "application/json")
                        .header("X-XSRF-TOKEN", csrfToken())
                        .POST(HttpRequest.BodyPublishers.ofString(json)).build(),
                HttpResponse.BodyHandlers.ofString());
    }

    HttpResponse<String> postWithoutCsrf(String path, String json) throws IOException, InterruptedException {
        return http.send(HttpRequest.newBuilder(uri(path))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(json)).build(),
                HttpResponse.BodyHandlers.ofString());
    }

    private String csrfToken() throws IOException, InterruptedException {
        var existing = cookies.getCookieStore().getCookies().stream().filter(c -> c.getName().equals("XSRF-TOKEN")).findFirst();
        if (existing.isEmpty()) {
            get("/api/auth/csrf");
        }
        return cookies.getCookieStore().getCookies().stream().filter(c -> c.getName().equals("XSRF-TOKEN"))
                .findFirst().orElseThrow(() -> new IllegalStateException("No XSRF-TOKEN cookie issued")).getValue();
    }

    private URI uri(String path) {
        return URI.create("http://localhost:" + port + path);
    }
}
