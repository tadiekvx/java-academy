package academy.content;

import java.util.Locale;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * An external learning resource from {@code resources.yaml}: a video, course, documentation page,
 * article or tool. Lessons reference resources by id. Nothing here is invented: {@code verifiedOn}
 * records when someone last opened the URL and confirmed it is what this entry says it is.
 */
public record Resource(
        String id,
        String title,
        String creator,
        String url,
        Kind kind,
        Level level,
        String topic,
        String why,
        @JsonProperty("youtube_id") String youtubeId,
        @JsonProperty("start_seconds") Integer startSeconds,
        String published,
        @JsonProperty("verified_on") String verifiedOn,
        String caveat) {

    public enum Kind { VIDEO, COURSE, DOCS, ARTICLE, TOOL;

        public String label() {
            return name().charAt(0) + name().substring(1).toLowerCase(Locale.ROOT);
        }
    }

    public enum Level { INTRODUCTORY, SUPPLEMENTARY, ADVANCED }

    /** Whether the page can show this as an embedded video (only YouTube ids that were verified). */
    public boolean embeddable() {
        return kind == Kind.VIDEO && youtubeId != null && !youtubeId.isBlank();
    }
}
