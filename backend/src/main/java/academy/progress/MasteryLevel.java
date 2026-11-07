package academy.progress;

/** Concept mastery levels from docs/curriculum/01-curriculum-design.md §4.3. */
public enum MasteryLevel {
    NOT_STARTED("Not started"),
    INTRODUCED("Introduced"),
    PRACTISING("Practising"),
    DEMONSTRATED("Demonstrated"),
    SECURE("Secure"),
    RETAINED("Retained");

    private final String label;

    MasteryLevel(String label) {
        this.label = label;
    }

    public String label() {
        return label;
    }
}
