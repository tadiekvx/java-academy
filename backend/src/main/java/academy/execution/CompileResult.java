package academy.execution;

import java.util.List;

/** The outcome of compiling a set of sources. {@code program} is null when compilation failed. */
public record CompileResult(List<Diagnostic> diagnostics, CompiledProgram program) {

    public boolean succeeded() {
        return program != null;
    }

    public List<Diagnostic> errors() {
        return diagnostics.stream().filter(d -> d.kind() == Diagnostic.Kind.ERROR).toList();
    }
}
