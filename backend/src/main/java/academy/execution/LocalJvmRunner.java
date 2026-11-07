package academy.execution;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.StringWriter;
import java.io.UncheckedIOException;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;

import javax.tools.DiagnosticCollector;
import javax.tools.JavaCompiler;
import javax.tools.JavaFileObject;
import javax.tools.StandardJavaFileManager;
import javax.tools.ToolProvider;

import org.springframework.stereotype.Component;

/**
 * Compiles learner code in-process with javac and runs it in a separate JVM process.
 *
 * <p><strong>Development only.</strong> The child process runs with the platform's own OS
 * permissions: it can read and write files and open network connections. The time, memory and
 * output limits protect the machine from accidents (infinite loops, runaway output), not from
 * malicious code. Replace this with a sandboxed runner before any untrusted user can submit code.
 */
@Component
public class LocalJvmRunner {

    private static final String JAVA_RELEASE = "25";
    private static final int MAX_CONCURRENT_RUNS = 4;

    /**
     * The in-memory database jar that Stage 6 exercises use. It is optional: everything
     * outside Stage 6 runs without it. This is a teaching convenience, not a sandbox.
     */
    private static final String DATABASE_JAR = locateJar("org/h2/Driver.class");

    private final JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
    private final Path javaExecutable = Path.of(System.getProperty("java.home"), "bin", "java");
    private final Semaphore runSlots = new Semaphore(MAX_CONCURRENT_RUNS);

    public CompileResult compile(List<SourceFile> sources) {
        Path workDir = createWorkDir();
        try {
            Path srcDir = Files.createDirectory(workDir.resolve("src"));
            Path classesDir = Files.createDirectory(workDir.resolve("classes"));
            List<Path> paths = new ArrayList<>();
            for (SourceFile source : sources) {
                paths.add(Files.writeString(srcDir.resolve(source.name()), source.content()));
            }

            var collector = new DiagnosticCollector<JavaFileObject>();
            boolean ok;
            try (StandardJavaFileManager files =
                         compiler.getStandardFileManager(collector, Locale.ENGLISH, StandardCharsets.UTF_8)) {
                List<String> options = List.of(
                        "--release", JAVA_RELEASE,
                        "-encoding", "UTF-8",
                        "-proc:none",
                        // An explicit class path stops javac inheriting the platform's own class path.
                        // The database jar is added deliberately, so learners can import JDBC helpers.
                        "-classpath", learnerClassPath(classesDir),
                        "-d", classesDir.toString());
                ok = compiler.getTask(new StringWriter(), files, collector, options, null,
                        files.getJavaFileObjectsFromPaths(paths)).call();
            }

            List<Diagnostic> diagnostics = collector.getDiagnostics().stream()
                    .filter(d -> d.getKind() == javax.tools.Diagnostic.Kind.ERROR
                            || d.getKind() == javax.tools.Diagnostic.Kind.WARNING
                            || d.getKind() == javax.tools.Diagnostic.Kind.MANDATORY_WARNING)
                    .map(LocalJvmRunner::toDiagnostic)
                    .toList();
            if (!ok) {
                CompiledProgram.deleteRecursively(workDir);
                return new CompileResult(diagnostics, null);
            }
            return new CompileResult(diagnostics, new CompiledProgram(workDir, classesDir));
        } catch (IOException e) {
            CompiledProgram.deleteRecursively(workDir);
            throw new UncheckedIOException(e);
        }
    }

    public RunResult run(CompiledProgram program, String mainClass, String stdin, ExecutionLimits limits) {
        List<String> command = List.of(
                javaExecutable.toString(),
                "-Xmx" + limits.memoryMb() + "m",
                "-Xss1m",
                "-XX:+UseSerialGC",
                "-XX:TieredStopAtLevel=1",
                "-XX:-UsePerfData",
                "-Dfile.encoding=UTF-8",
                "-Dstdout.encoding=UTF-8",
                "-Dstderr.encoding=UTF-8",
                "-cp", learnerClassPath(program.classesDir()),
                mainClass);
        var builder = new ProcessBuilder(command).directory(program.workDir().toFile());
        // Learner code must not see the platform's environment, which holds secrets such as API keys.
        builder.environment().clear();

        runSlots.acquireUninterruptibly();
        try {
            long start = System.nanoTime();
            Process process = builder.start();
            var stdout = new BoundedCapture(process.getInputStream(), limits.maxOutputBytes(), () -> kill(process));
            var stderr = new BoundedCapture(process.getErrorStream(), limits.maxOutputBytes(), () -> kill(process));
            Thread stdoutReader = Thread.ofVirtual().start(stdout);
            Thread stderrReader = Thread.ofVirtual().start(stderr);
            Thread stdinWriter = Thread.ofVirtual().start(() -> writeQuietly(process.getOutputStream(), stdin));

            boolean finished = process.waitFor(limits.timeout().toMillis(), TimeUnit.MILLISECONDS);
            if (!finished) {
                kill(process);
            }
            int exitCode = process.waitFor();
            stdoutReader.join();
            stderrReader.join();
            stdinWriter.join();
            return new RunResult(exitCode, stdout.text(), stderr.text(), !finished,
                    stdout.overflowed() || stderr.overflowed(), Duration.ofNanos(System.nanoTime() - start));
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("Interrupted while running learner code", e);
        } finally {
            runSlots.release();
        }
    }

    private static String learnerClassPath(Path classesDir) {
        return DATABASE_JAR == null
                ? classesDir.toString()
                : classesDir + File.pathSeparator + DATABASE_JAR;
    }

    /**
     * Finds a jar on the platform's own class path from a class it contains. Returns null
     * when the class isn't there (for example in a packaged build, where the dependency is
     * nested inside the executable jar) so that all non-database content keeps working.
     */
    private static String locateJar(String resource) {
        URL url = LocalJvmRunner.class.getClassLoader().getResource(resource);
        if (url == null || !"jar".equals(url.getProtocol())) {
            return null;
        }
        String location = url.toString().substring("jar:".length());
        int separator = location.indexOf("!/");
        if (separator < 0) {
            return null;
        }
        String jar = location.substring(0, separator);
        if (jar.contains("!/")) {
            return null;  // nested inside a Spring Boot executable jar; not extracted here
        }
        try {
            return Path.of(URI.create(jar)).toString();
        } catch (IllegalArgumentException e) {
            return null;
        }
    }

    private static Diagnostic toDiagnostic(javax.tools.Diagnostic<? extends JavaFileObject> d) {
        String file = d.getSource() == null ? null : Path.of(d.getSource().toUri()).getFileName().toString();
        var kind = d.getKind() == javax.tools.Diagnostic.Kind.ERROR ? Diagnostic.Kind.ERROR : Diagnostic.Kind.WARNING;
        long line = d.getLineNumber() == javax.tools.Diagnostic.NOPOS ? -1 : d.getLineNumber();
        long column = d.getColumnNumber() == javax.tools.Diagnostic.NOPOS ? -1 : d.getColumnNumber();
        return new Diagnostic(file, line, column, kind, d.getMessage(Locale.ENGLISH));
    }

    private static Path createWorkDir() {
        try {
            return Files.createTempDirectory("academy-run-");
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    private static void kill(Process process) {
        process.descendants().forEach(ProcessHandle::destroyForcibly);
        process.destroyForcibly();
    }

    private static void writeQuietly(OutputStream out, String text) {
        try (out) {
            out.write(text.getBytes(StandardCharsets.UTF_8));
        } catch (IOException e) {
            // The program exited without reading all of its input; that is the program's business.
        }
    }

    /** Reads a stream to the end, keeping at most {@code limit} bytes and reporting the first overflow. */
    private static final class BoundedCapture implements Runnable {

        private final InputStream in;
        private final int limit;
        private final Runnable onOverflow;
        private final ByteArrayOutputStream kept = new ByteArrayOutputStream();
        private volatile boolean overflowed;

        BoundedCapture(InputStream in, int limit, Runnable onOverflow) {
            this.in = in;
            this.limit = limit;
            this.onOverflow = onOverflow;
        }

        @Override
        public void run() {
            byte[] buffer = new byte[8192];
            try (in) {
                int n;
                while ((n = in.read(buffer)) != -1) {
                    int room = limit - kept.size();
                    kept.write(buffer, 0, Math.min(room, n));
                    if (n > room && !overflowed) {
                        overflowed = true;
                        onOverflow.run();
                    }
                }
            } catch (IOException e) {
                // Stream closed because the process was killed.
            }
        }

        String text() {
            return kept.toString(StandardCharsets.UTF_8);
        }

        boolean overflowed() {
            return overflowed;
        }
    }
}
