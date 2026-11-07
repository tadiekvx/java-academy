package academy;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.springframework.boot.SpringApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Primary;

import academy.mentor.MentorModel;

/**
 * Runs the platform with a scripted stand-in for the mentor model, for working on the mentor UI
 * without an API key: {@code mvn spring-boot:test-run}. It answers according to the granted help
 * level, so every part of the flow (gates, code checks, follow-ups) can be exercised by hand.
 * Never used in production: it lives in the test sources.
 */
public class DemoMentorApplication {

    public static void main(String[] args) {
        SpringApplication.from(AcademyApplication::main).with(DemoModelConfig.class).run(args);
    }

    // @TestConfiguration keeps this out of component scanning, so other tests don't pick it up.
    @TestConfiguration
    static class DemoModelConfig {

        @Bean
        @Primary
        MentorModel demoMentorModel() {
            return new DemoMentorModel();
        }
    }

    static class DemoMentorModel implements MentorModel {

        private static final Pattern LEVEL = Pattern.compile("GRANTED HELP LEVEL: (H\\d)");
        private static final Pattern SOLUTION = Pattern.compile("REFERENCE SOLUTION[^\\n]*\\n(.*)$", Pattern.DOTALL);

        @Override
        public boolean available() {
            return true;
        }

        @Override
        public String id() {
            return "demo-scripted-model";
        }

        @Override
        public MentorReply reply(String context, List<Turn> history, String request) {
            boolean solutionRequest = request.toLowerCase().contains("give me") || request.toLowerCase().contains("the answer");
            if (request.startsWith("FOLLOW-UP CHECK")) {
                return new MentorReply("*(Demo model)* What would your method return for `percentage(1, 3)`, and why?", "", "", false);
            }
            Matcher level = LEVEL.matcher(request);
            String granted = level.find() ? level.group(1) : "H1";
            return switch (granted) {
                case "H2" -> new MentorReply("*(Demo model, H2)* Look at `correct / total`. Both are `int`s, so what does "
                        + "Java do with the fraction **before** the `* 100` happens?", "", "", solutionRequest);
                case "H3" -> new MentorReply("*(Demo model, H3)* Here's a similar problem: half of a total, exactly. Notice "
                        + "which side of the division is a `double`.",
                        "double halfOf(int total) {\n    return total / 2.0;\n}\n\nvoid main() {\n    IO.println(halfOf(7));\n}\n",
                        "3.5", solutionRequest);
                case "H4" -> {
                    Matcher solution = SOLUTION.matcher(context);
                    yield new MentorReply("*(Demo model, H4)* Here's a full solution. Each step: convert to `double` first, "
                            + "then divide, then scale.", solution.find() ? solution.group(1).strip() : "", "", false);
                }
                default -> new MentorReply("*(Demo model, " + granted + ")* Which lesson idea is this exercise about? "
                        + "Think about what happens when you divide two whole numbers.", "", "", solutionRequest);
            };
        }

        @Override
        public RubricScore score(String rubricPrompt) {
            return new RubricScore(2, "Demo model: always scores 2.", "*(Demo model)* Clear explanation. In real use, the AI mentor scores this against the rubric.");
        }
    }
}
