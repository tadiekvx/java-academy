package academy.api;

import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import academy.learner.AccountService;
import academy.mentor.MentorUnavailableException;

/** Turns expected failures into JSON errors with learner-facing messages. */
@RestControllerAdvice
class ApiErrors {

    @ExceptionHandler(IllegalArgumentException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    Map<String, String> badRequest(IllegalArgumentException e) {
        return Map.of("error", e.getMessage());
    }

    @ExceptionHandler(AccountService.EmailTakenException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    Map<String, String> emailTaken(AccountService.EmailTakenException e) {
        return Map.of("error", e.getMessage());
    }

    @ExceptionHandler(MentorUnavailableException.class)
    @ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
    Map<String, String> mentorUnavailable(MentorUnavailableException e) {
        return Map.of("error", e.getMessage());
    }

    @ExceptionHandler(AuthenticationException.class)
    @ResponseStatus(HttpStatus.UNAUTHORIZED)
    Map<String, String> loginFailed() {
        return Map.of("error", "That email and password don't match an account.");
    }
}
