package academy.execution;

/** A single Java source file, identified by its simple file name (e.g. {@code Main.java}). */
public record SourceFile(String name, String content) {

    public SourceFile {
        if (!name.matches("[A-Za-z_$][A-Za-z0-9_$]*\\.java")) {
            throw new IllegalArgumentException("Not a simple Java source file name: " + name);
        }
    }
}
