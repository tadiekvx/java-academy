package academy.progress;

import java.time.Instant;
import java.time.OffsetDateTime;
import java.time.ZoneOffset;
import java.util.Set;

import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Repository;

@Repository
class LessonVisitRepository {

    private final JdbcClient jdbc;

    LessonVisitRepository(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    void record(long learnerId, String lessonId, Instant now) {
        jdbc.sql("""
                        insert into lesson_visit (learner_id, lesson_id, first_visited_at)
                        values (:learnerId, :lessonId, :now)
                        on conflict do nothing""")
                .param("learnerId", learnerId)
                .param("lessonId", lessonId)
                .param("now", OffsetDateTime.ofInstant(now, ZoneOffset.UTC))
                .update();
    }

    Set<String> visitedLessons(long learnerId) {
        return Set.copyOf(jdbc.sql("select lesson_id from lesson_visit where learner_id = :learnerId")
                .param("learnerId", learnerId)
                .query(String.class)
                .list());
    }

    /** Lessons the learner has marked finished by hand. */
    Set<String> markedComplete(long learnerId) {
        return Set.copyOf(jdbc.sql("select lesson_id from lesson_visit where learner_id = :learnerId and completed_at is not null")
                .param("learnerId", learnerId)
                .query(String.class)
                .list());
    }

    void setCompleted(long learnerId, String lessonId, Instant now, boolean completed) {
        jdbc.sql("""
                        insert into lesson_visit (learner_id, lesson_id, first_visited_at, completed_at)
                        values (:learnerId, :lessonId, :now, :completedAt)
                        on conflict (learner_id, lesson_id) do update set completed_at = excluded.completed_at""")
                .param("learnerId", learnerId)
                .param("lessonId", lessonId)
                .param("now", OffsetDateTime.ofInstant(now, ZoneOffset.UTC))
                .param("completedAt", completed ? OffsetDateTime.ofInstant(now, ZoneOffset.UTC) : null)
                .update();
    }
}
