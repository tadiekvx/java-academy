package academy.progress;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.Instant;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

import academy.assessment.GradeReport;

@Repository
public class AttemptRepository {

    private final JdbcClient jdbc;

    AttemptRepository(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    long record(long learnerId, String exerciseId, Instant submittedAt, AttemptContext context, GradeReport report,
            int assistanceLevel, boolean solutionViewed, String submissionJson, String reportJson) {
        int passed = (int) report.tests().stream().filter(t -> t.passed()).count();
        return jdbc.sql("""
                        insert into attempt (learner_id, exercise_id, submitted_at, context, outcome, tests_passed,
                                             tests_total, assistance_level, solution_viewed, submission, report)
                        values (:learnerId, :exerciseId, :submittedAt, :context, :outcome, :testsPassed,
                                :testsTotal, :assistanceLevel, :solutionViewed, cast(:submission as jsonb), cast(:report as jsonb))
                        returning id""")
                .param("learnerId", learnerId)
                .param("exerciseId", exerciseId)
                .param("submittedAt", OffsetDateTime.ofInstant(submittedAt, ZoneOffset.UTC))
                .param("context", context.dbValue())
                .param("outcome", report.outcome().name())
                .param("testsPassed", passed)
                .param("testsTotal", report.tests().size())
                .param("assistanceLevel", assistanceLevel)
                .param("solutionViewed", solutionViewed)
                .param("submission", submissionJson)
                .param("report", reportJson)
                .query(Long.class)
                .single();
    }

    /** All of a learner's attempts, oldest first. */
    public List<Attempt> forLearner(long learnerId) {
        return jdbc.sql("select *, md5(submission::text) as submission_hash from attempt where learner_id = :learnerId order by submitted_at, id")
                .param("learnerId", learnerId)
                .query(AttemptRepository::map)
                .list();
    }

    /** A learner's most recent attempt at each exercise: what they submitted and what they were shown. */
    record Saved(String exerciseId, Instant submittedAt, String submissionJson, String reportJson) {}

    Map<String, Saved> latestByExercise(long learnerId) {
        return jdbc.sql("""
                        select distinct on (exercise_id) exercise_id, submitted_at, submission::text as submission, report::text as report
                        from attempt where learner_id = :learnerId and context = 'practice'
                        order by exercise_id, submitted_at desc, id desc""")
                .param("learnerId", learnerId)
                .query((rs, row) -> new Saved(rs.getString("exercise_id"),
                        rs.getObject("submitted_at", OffsetDateTime.class).toInstant(), rs.getString("submission"),
                        rs.getString("report")))
                .list().stream().collect(Collectors.toMap(Saved::exerciseId, saved -> saved));
    }

    private static Attempt map(ResultSet rs, int row) throws SQLException {
        return new Attempt(
                rs.getLong("id"),
                rs.getLong("learner_id"),
                rs.getString("exercise_id"),
                rs.getObject("submitted_at", OffsetDateTime.class).toInstant(),
                AttemptContext.fromDb(rs.getString("context")),
                GradeReport.Outcome.valueOf(rs.getString("outcome")),
                rs.getInt("tests_passed"),
                rs.getInt("tests_total"),
                rs.getInt("assistance_level"),
                rs.getBoolean("solution_viewed"),
                rs.getString("submission_hash"));
    }
}
