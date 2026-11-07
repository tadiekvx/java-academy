package academy.execution;

import java.time.Duration;

public record ExecutionLimits(Duration timeout, int memoryMb, int maxOutputBytes) {

    public static final ExecutionLimits DEFAULT = new ExecutionLimits(Duration.ofSeconds(5), 128, 64 * 1024);

    public ExecutionLimits withTimeout(Duration newTimeout) {
        return new ExecutionLimits(newTimeout, memoryMb, maxOutputBytes);
    }
}
