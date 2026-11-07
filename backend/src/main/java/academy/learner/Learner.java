package academy.learner;

import java.time.Instant;

public record Learner(
        long id,
        String email,
        String displayName,
        Instant createdAt,
        Instant onboardedAt,
        String experience,
        Integer weeklyHours,
        String goal) {

    public boolean onboarded() {
        return onboardedAt != null;
    }
}
