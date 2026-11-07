package academy.mentor;

public class MentorUnavailableException extends RuntimeException {

    public MentorUnavailableException(String message) {
        super(message);
    }

    public MentorUnavailableException(String message, Throwable cause) {
        super(message, cause);
    }
}
