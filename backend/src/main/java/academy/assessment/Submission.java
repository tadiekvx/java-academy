package academy.assessment;

import java.util.List;
import java.util.Map;

/**
 * What a learner submits. Which fields are used depends on the exercise type: {@code files} for
 * code exercises, {@code prediction} for predict, {@code order} (indices into the Parsons palette)
 * for Parsons, {@code explanation} for explain.
 */
public record Submission(Map<String, String> files, String prediction, List<Integer> order, String explanation) {

    public static Submission ofFiles(Map<String, String> files) {
        return new Submission(files, null, null, null);
    }
}
