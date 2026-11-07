package academy.content;

public enum ExerciseType {
    PREDICT, PARSONS, WRITE, DEBUG, MODIFY, EXPLAIN;

    /** Whether the learner submits Java source that is graded by tests. */
    public boolean isCodeExercise() {
        return this == WRITE || this == DEBUG || this == MODIFY;
    }
}
