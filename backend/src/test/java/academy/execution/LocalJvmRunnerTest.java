package academy.execution;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.util.List;

import org.junit.jupiter.api.Test;

class LocalJvmRunnerTest {

    private final LocalJvmRunner runner = new LocalJvmRunner();

    @Test
    void reportsCompileErrorsWithPosition() {
        CompileResult result = runner.compile(List.of(new SourceFile("Main.java", """
                void main() {
                    IO.println("missing semicolon")
                }
                """)));

        assertThat(result.succeeded()).isFalse();
        assertThat(result.errors()).singleElement().satisfies(d -> {
            assertThat(d.file()).isEqualTo("Main.java");
            assertThat(d.line()).isEqualTo(2);
            assertThat(d.message()).contains("';' expected");
        });
    }

    @Test
    void runsCompactSourceFileWithInput() {
        String output = run("""
                void main() {
                    String name = IO.readln("Name? ");
                    IO.println("Hello, " + name);
                }
                """, "Ada\n", ExecutionLimits.DEFAULT).stdout();

        assertThat(output).isEqualTo("Name? Hello, Ada\n");
    }

    @Test
    void stopsProgramsThatRunTooLong() {
        RunResult result = run("""
                void main() {
                    while (true) { }
                }
                """, "", ExecutionLimits.DEFAULT.withTimeout(Duration.ofSeconds(1)));

        assertThat(result.timedOut()).isTrue();
        assertThat(result.completedNormally()).isFalse();
    }

    @Test
    void stopsProgramsThatPrintTooMuch() {
        RunResult result = run("""
                void main() {
                    while (true) { IO.println("again and again"); }
                }
                """, "", ExecutionLimits.DEFAULT);

        assertThat(result.outputLimitExceeded()).isTrue();
        assertThat(result.stdout().length()).isLessThanOrEqualTo(ExecutionLimits.DEFAULT.maxOutputBytes());
    }

    @Test
    void hidesThePlatformEnvironmentFromLearnerCode() {
        String output = run("""
                void main() {
                    IO.println(System.getenv("HOME") + " " + System.getenv("PATH") + " " + System.getenv("USER"));
                }
                """, "", ExecutionLimits.DEFAULT).stdout();

        assertThat(output.strip()).isEqualTo("null null null");
    }

    @Test
    void makesTheInMemoryDatabaseAvailableToLearnerCode() {
        String output = run("""
                import java.sql.Connection;
                import java.sql.DriverManager;
                import java.sql.PreparedStatement;
                import java.sql.ResultSet;

                void main() throws Exception {
                    try (Connection connection = DriverManager.getConnection(
                            "jdbc:h2:mem:runnertest;DB_CLOSE_DELAY=-1")) {
                        connection.createStatement().execute(
                                "CREATE TABLE account (id INT PRIMARY KEY, balance BIGINT NOT NULL)");
                        try (PreparedStatement insert = connection.prepareStatement(
                                "INSERT INTO account (id, balance) VALUES (?, ?)")) {
                            insert.setInt(1, 1);
                            insert.setLong(2, 500);
                            insert.executeUpdate();
                        }
                        try (ResultSet rows = connection.createStatement().executeQuery(
                                "SELECT id, balance FROM account")) {
                            while (rows.next()) {
                                IO.println(rows.getInt("id") + "|" + rows.getLong("balance"));
                            }
                        }
                    }
                }
                """, "", ExecutionLimits.DEFAULT).stdout();

        assertThat(output.strip()).isEqualTo("1|500");
    }

    @Test
    void doesNotExposeThePlatformClassPathToTheCompiler() {
        CompileResult result = runner.compile(List.of(new SourceFile("Main.java", """
                void main() {
                    IO.println(org.springframework.util.StringUtils.hasText("x"));
                }
                """)));

        assertThat(result.succeeded()).isFalse();
    }

    private RunResult run(String source, String stdin, ExecutionLimits limits) {
        CompileResult compiled = runner.compile(List.of(new SourceFile("Main.java", source)));
        assertThat(compiled.errors()).isEmpty();
        try (CompiledProgram program = compiled.program()) {
            return runner.run(program, "Main", stdin, limits);
        }
    }
}
