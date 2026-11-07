package academy.content;

import java.nio.file.Path;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Where content lives, and whether learners may see lessons that are not yet published
 * (useful in development and for reviewers; must be false in production).
 */
@ConfigurationProperties("academy.content")
public record ContentProperties(String root, String sources, boolean showUnpublished) {

    // Bound as strings: Spring's String-to-Path conversion treats values as resource locations,
    // which rejects relative paths such as ../content/java.

    public Path rootPath() {
        return Path.of(root);
    }

    public Path sourcesPath() {
        return Path.of(sources);
    }
}
