package academy.content;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Source IDs and their verification status, read from the table rows of
 * {@code docs/curriculum/sources.md}, which stays the single source of truth.
 */
public record SourceRegister(Map<String, Boolean> verifiedById) {

    private static final Pattern ROW = Pattern.compile("^\\| ([RIC]\\d+) \\|.*\\|([^|]*)\\|\\s*$");

    public static SourceRegister parse(Path file) {
        Map<String, Boolean> entries = new LinkedHashMap<>();
        try {
            for (String line : Files.readAllLines(file)) {
                Matcher m = ROW.matcher(line);
                if (m.matches()) {
                    entries.put(m.group(1), m.group(2).contains("**Verified"));
                }
            }
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        return new SourceRegister(entries);
    }

    public Optional<Boolean> isVerified(String id) {
        return Optional.ofNullable(verifiedById.get(id));
    }
}
