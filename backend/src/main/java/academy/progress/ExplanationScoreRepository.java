package academy.progress;

import java.time.Instant;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

/** Rubric scores for written explanations, keyed by the attempt they score. */
@Repository
public class ExplanationScoreRepository {

    private final JdbcClient jdbc;

    ExplanationScoreRepository(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    public void record(long attemptId, int score, String rationale, String feedback, String scoredBy, boolean provisional,
            Instant at) {
        jdbc.sql("""
                        insert into explanation_score (attempt_id, score, rationale, feedback, scored_by, provisional, scored_at)
                        values (:attemptId, :score, :rationale, :feedback, :scoredBy, :provisional, :at)""")
                .param("attemptId", attemptId)
                .param("score", score)
                .param("rationale", rationale)
                .param("feedback", feedback)
                .param("scoredBy", scoredBy)
                .param("provisional", provisional)
                .param("at", OffsetDateTime.ofInstant(at, ZoneOffset.UTC))
                .update();
    }

    /** Scores for all of a learner's scored attempts, by attempt id. */
    Map<Long, Integer> forLearner(long learnerId) {
        return jdbc.sql("""
                        select s.attempt_id, s.score from explanation_score s
                        join attempt a on a.id = s.attempt_id
                        where a.learner_id = :learnerId""")
                .param("learnerId", learnerId)
                .query((rs, n) -> Map.entry(rs.getLong(1), rs.getInt(2)))
                .list().stream()
                .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
    }
}
