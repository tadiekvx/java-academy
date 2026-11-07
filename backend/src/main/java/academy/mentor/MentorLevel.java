package academy.mentor;

/** Assistance levels H0–H4 from docs/curriculum/04-ai-mentor-policy.md §1. */
public enum MentorLevel {
    CLARIFY("Clarify", "Restates what the task asks and explains words in the prompt."),
    NUDGE("Nudge", "Points to the idea or pattern you need, with a guiding question."),
    TARGETED_HINT("Targeted hint", "Says which part of your code is wrong and what the error or failing test means."),
    WORKED_EXAMPLE("Worked example", "Shows a similar, different problem worked through, with code."),
    WALKTHROUGH("Walkthrough", "Walks through a solution to this exercise. It won't count towards mastery.");

    /** The highest level that still counts as independent work. */
    public static final MentorLevel MAX_INDEPENDENT = NUDGE;

    private final String label;
    private final String description;

    MentorLevel(String label, String description) {
        this.label = label;
        this.description = description;
    }

    public int number() {
        return ordinal();
    }

    public String code() {
        return "H" + ordinal();
    }

    public String label() {
        return label;
    }

    public String description() {
        return description;
    }

    public static MentorLevel of(int number) {
        return values()[number];
    }

    public MentorLevel next() {
        return this == WALKTHROUGH ? WALKTHROUGH : values()[ordinal() + 1];
    }
}
