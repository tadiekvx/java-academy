package academy.content;

/** A problem found while loading or validating content. {@code location} names the file or item. */
public record Issue(Severity severity, String location, String message) {

    public enum Severity { ERROR, WARNING }

    public static Issue error(String location, String message) {
        return new Issue(Severity.ERROR, location, message);
    }

    public static Issue warning(String location, String message) {
        return new Issue(Severity.WARNING, location, message);
    }
}
