package academy.content;

public enum LessonStatus {
    DRAFT, IN_REVIEW, PUBLISHED, RETIRED;

    /** Whether the content is meant to meet the full publication standard (it is published, or submitted for review). */
    public boolean heldToPublicationStandard() {
        return this == IN_REVIEW || this == PUBLISHED;
    }
}
