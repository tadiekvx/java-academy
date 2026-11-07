package academy.mentor;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.Instant;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

@Repository
class MentorRepository {

    private final JdbcClient jdbc;

    MentorRepository(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    enum Kind { QUESTION, HELP, FOLLOW_UP_QUESTION, FOLLOW_UP_ANSWER, FOLLOW_UP_FEEDBACK }

    record Message(
            long id,
            String exerciseId,
            Instant createdAt,
            boolean fromLearner,
            Kind kind,
            int level,
            String content,
            String code,
            String codeCheck,
            boolean solutionRequest,
            Integer score) {}

    record NewMessage(long learnerId, String exerciseId, Instant at, boolean fromLearner, Kind kind, int level,
            String content, String code, String codeCheck, boolean solutionRequest, Integer score, String model) {}

    void insert(NewMessage m) {
        jdbc.sql("""
                        insert into mentor_message (learner_id, exercise_id, created_at, role, kind, level, content, code,
                                                    code_check, solution_request, score, model)
                        values (:learnerId, :exerciseId, :at, :role, :kind, :level, :content, :code,
                                :codeCheck, :solutionRequest, :score, :model)""")
                .param("learnerId", m.learnerId())
                .param("exerciseId", m.exerciseId())
                .param("at", OffsetDateTime.ofInstant(m.at(), ZoneOffset.UTC))
                .param("role", m.fromLearner() ? "learner" : "mentor")
                .param("kind", m.kind().name().toLowerCase())
                .param("level", m.level())
                .param("content", m.content())
                .param("code", m.code())
                .param("codeCheck", m.codeCheck())
                .param("solutionRequest", m.solutionRequest())
                .param("score", m.score())
                .param("model", m.model())
                .update();
    }

    /** All of a learner's mentor messages, oldest first. */
    List<Message> forLearner(long learnerId) {
        return jdbc.sql("select * from mentor_message where learner_id = :learnerId order by created_at, id")
                .param("learnerId", learnerId)
                .query(MentorRepository::map)
                .list();
    }

    /** Model calls made for the learner since {@code since}: every mentor-authored message is one call. */
    int modelCallsSince(long learnerId, Instant since) {
        return jdbc.sql("select count(*) from mentor_message where learner_id = :learnerId and role = 'mentor' and created_at >= :since")
                .param("learnerId", learnerId)
                .param("since", OffsetDateTime.ofInstant(since, ZoneOffset.UTC))
                .query(Integer.class)
                .single();
    }

    private static Message map(ResultSet rs, int row) throws SQLException {
        return new Message(
                rs.getLong("id"),
                rs.getString("exercise_id"),
                rs.getObject("created_at", OffsetDateTime.class).toInstant(),
                rs.getString("role").equals("learner"),
                Kind.valueOf(rs.getString("kind").toUpperCase()),
                rs.getInt("level"),
                rs.getString("content"),
                rs.getString("code"),
                rs.getString("code_check"),
                rs.getBoolean("solution_request"),
                rs.getObject("score", Integer.class));
    }
}
