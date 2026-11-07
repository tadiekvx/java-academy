package academy.learner;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.Instant;
import java.time.OffsetDateTime;
import java.util.Optional;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

@Repository
public class LearnerRepository {

    private final JdbcClient jdbc;

    LearnerRepository(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    long create(String email, String displayName, String passwordHash, Instant now) {
        return jdbc.sql("""
                        insert into learner (email, display_name, password_hash, created_at)
                        values (:email, :displayName, :passwordHash, :now)
                        returning id""")
                .param("email", email)
                .param("displayName", displayName)
                .param("passwordHash", passwordHash)
                .param("now", OffsetDateTime.ofInstant(now, java.time.ZoneOffset.UTC))
                .query(Long.class)
                .single();
    }

    boolean emailExists(String email) {
        return jdbc.sql("select exists (select 1 from learner where email = :email)")
                .param("email", email)
                .query(Boolean.class)
                .single();
    }

    public Optional<Learner> findById(long id) {
        return jdbc.sql("select * from learner where id = :id").param("id", id).query(LearnerRepository::map).optional();
    }

    /** The learner's id and password hash, for authentication. */
    Optional<Credentials> findCredentials(String email) {
        return jdbc.sql("select id, password_hash from learner where email = :email")
                .param("email", email)
                .query((rs, n) -> new Credentials(rs.getLong("id"), rs.getString("password_hash")))
                .optional();
    }

    record Credentials(long id, String passwordHash) {}

    void completeOnboarding(long id, String experience, int weeklyHours, String goal, Instant now) {
        jdbc.sql("""
                        update learner
                        set experience = :experience, weekly_hours = :weeklyHours, goal = :goal,
                            onboarded_at = coalesce(onboarded_at, :now)
                        where id = :id""")
                .param("experience", experience)
                .param("weeklyHours", weeklyHours)
                .param("goal", goal)
                .param("now", OffsetDateTime.ofInstant(now, java.time.ZoneOffset.UTC))
                .param("id", id)
                .update();
    }

    private static Learner map(ResultSet rs, int row) throws SQLException {
        OffsetDateTime onboarded = rs.getObject("onboarded_at", OffsetDateTime.class);
        return new Learner(
                rs.getLong("id"),
                rs.getString("email"),
                rs.getString("display_name"),
                rs.getObject("created_at", OffsetDateTime.class).toInstant(),
                onboarded == null ? null : onboarded.toInstant(),
                rs.getString("experience"),
                rs.getObject("weekly_hours", Integer.class),
                rs.getString("goal"));
    }
}
