package academy.mentor;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

/** A scripted mentor model for tests: returns queued replies and records what it was asked. */
public class FakeMentorModel implements MentorModel {

    public final Deque<MentorReply> replies = new ArrayDeque<>();
    public final Deque<RubricScore> scores = new ArrayDeque<>();
    public final List<String> contexts = new ArrayList<>();
    public final List<String> requests = new ArrayList<>();
    public boolean available = true;

    public void reset() {
        replies.clear();
        scores.clear();
        contexts.clear();
        requests.clear();
        available = true;
    }

    @Override
    public boolean available() {
        return available;
    }

    @Override
    public String id() {
        return "fake-model";
    }

    @Override
    public MentorReply reply(String context, List<Turn> history, String request) {
        contexts.add(context);
        requests.add(request);
        return replies.isEmpty() ? new MentorReply("Think about the types involved.", "", "", false) : replies.removeFirst();
    }

    @Override
    public RubricScore score(String rubricPrompt) {
        requests.add(rubricPrompt);
        return scores.isEmpty() ? new RubricScore(1, "Partly right.", "Good start.") : scores.removeFirst();
    }
}
