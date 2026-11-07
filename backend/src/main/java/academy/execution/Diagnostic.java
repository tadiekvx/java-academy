package academy.execution;

/** A compiler message attached to a source position. Line and column are 1-based, or -1 when unknown. */
public record Diagnostic(String file, long line, long column, Kind kind, String message) {

    public enum Kind { ERROR, WARNING }
}
