package academy.learner;

import java.nio.charset.StandardCharsets;
import java.time.Clock;
import java.util.List;
import java.util.Locale;
import java.util.regex.Pattern;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

/** Registration and onboarding. Validation failures are {@link IllegalArgumentException}s with learner-facing messages. */
@Service
public class AccountService {

    public static final List<String> EXPERIENCE = List.of("none", "other-language", "some-java");
    public static final List<String> GOALS = List.of("career-change", "current-job", "study", "curiosity");

    private static final Pattern EMAIL = Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$");
    private static final int MIN_PASSWORD_LENGTH = 10;
    // BCrypt only uses the first 72 bytes of a password; reject longer ones rather than silently truncating.
    private static final int MAX_PASSWORD_BYTES = 72;

    private final LearnerRepository learners;
    private final PasswordEncoder passwordEncoder;
    private final Clock clock;

    AccountService(LearnerRepository learners, PasswordEncoder passwordEncoder, Clock clock) {
        this.learners = learners;
        this.passwordEncoder = passwordEncoder;
        this.clock = clock;
    }

    /**
     * @throws EmailTakenException if an account already uses the email address
     */
    public long register(String email, String displayName, String password) {
        String normalisedEmail = normaliseEmail(email);
        if (!EMAIL.matcher(normalisedEmail).matches()) {
            throw new IllegalArgumentException("Enter a valid email address.");
        }
        String name = displayName == null ? "" : displayName.strip();
        if (name.isEmpty() || name.length() > 60) {
            throw new IllegalArgumentException("Enter a name between 1 and 60 characters.");
        }
        if (password == null || password.length() < MIN_PASSWORD_LENGTH) {
            throw new IllegalArgumentException("Use a password of at least " + MIN_PASSWORD_LENGTH + " characters.");
        }
        if (password.getBytes(StandardCharsets.UTF_8).length > MAX_PASSWORD_BYTES) {
            throw new IllegalArgumentException("That password is too long. Use at most 72 characters.");
        }
        if (learners.emailExists(normalisedEmail)) {
            throw new EmailTakenException();
        }
        return learners.create(normalisedEmail, name, passwordEncoder.encode(password), clock.instant());
    }

    public void completeOnboarding(long learnerId, String experience, Integer weeklyHours, String goal) {
        if (!EXPERIENCE.contains(experience)) {
            throw new IllegalArgumentException("Choose how much programming you've done before.");
        }
        if (weeklyHours == null || weeklyHours < 1 || weeklyHours > 40) {
            throw new IllegalArgumentException("Choose how many hours a week you can study (1–40).");
        }
        if (!GOALS.contains(goal)) {
            throw new IllegalArgumentException("Choose what you're learning Java for.");
        }
        learners.completeOnboarding(learnerId, experience, weeklyHours, goal, clock.instant());
    }

    public static String normaliseEmail(String email) {
        return email == null ? "" : email.strip().toLowerCase(Locale.ROOT);
    }

    public static class EmailTakenException extends RuntimeException {

        EmailTakenException() {
            super("An account with this email address already exists. Try logging in instead.");
        }
    }
}
