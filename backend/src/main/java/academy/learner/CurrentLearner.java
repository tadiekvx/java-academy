package academy.learner;

import java.util.Optional;

import org.springframework.security.authentication.AnonymousAuthenticationToken;
import org.springframework.security.core.Authentication;

/** Reads the learner id from an authentication created by {@link LearnerDetailsService}. */
public final class CurrentLearner {

    private CurrentLearner() {}

    public static Optional<Long> id(Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated() || authentication instanceof AnonymousAuthenticationToken) {
            return Optional.empty();
        }
        return Optional.of(Long.parseLong(authentication.getName()));
    }

    public static long require(Authentication authentication) {
        return id(authentication).orElseThrow(() -> new IllegalStateException("No learner is logged in"));
    }
}
