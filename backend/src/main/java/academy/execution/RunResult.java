package academy.execution;

import java.time.Duration;

public record RunResult(
        int exitCode,
        String stdout,
        String stderr,
        boolean timedOut,
        boolean outputLimitExceeded,
        Duration elapsed) {

    public boolean completedNormally() {
        return exitCode == 0 && !timedOut && !outputLimitExceeded;
    }
}
