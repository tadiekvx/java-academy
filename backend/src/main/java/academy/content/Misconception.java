package academy.content;

import java.util.List;

public record Misconception(String id, String summary, List<String> concepts, String source) {}
