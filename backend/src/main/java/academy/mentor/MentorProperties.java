package academy.mentor;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * @param model Claude model id for the mentor
 * @param dailyRequestLimit model calls allowed per learner per day (a cost guard)
 */
@ConfigurationProperties("academy.mentor")
public record MentorProperties(String model, int dailyRequestLimit) {

    public MentorProperties {
        model = model == null || model.isBlank() ? "claude-opus-5-5" : model;
        dailyRequestLimit = dailyRequestLimit <= 0 ? 60 : dailyRequestLimit;
    }
}
