package academy.content;

import java.util.List;

public record Concept(String id, String name, List<String> prerequisites, List<Evidence> requiredEvidence) {}
