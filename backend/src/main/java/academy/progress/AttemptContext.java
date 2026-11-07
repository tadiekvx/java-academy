package academy.progress;

/** Where an attempt was made: a lesson exercise, or a scheduled retrieval check. */
public enum AttemptContext {
    PRACTICE, RETRIEVAL;

    String dbValue() {
        return name().toLowerCase();
    }

    static AttemptContext fromDb(String value) {
        return valueOf(value.toUpperCase());
    }
}
