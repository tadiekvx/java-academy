package academy.api;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContext;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.context.SecurityContextRepository;
import org.springframework.security.web.csrf.CsrfToken;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import academy.learner.AccountService;
import academy.learner.CurrentLearner;
import academy.learner.Learner;
import academy.learner.LearnerRepository;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@RestController
@RequestMapping("/api")
class AuthController {

    private final AccountService accounts;
    private final LearnerRepository learners;
    private final AuthenticationManager authenticationManager;
    private final SecurityContextRepository securityContextRepository;

    AuthController(AccountService accounts, LearnerRepository learners, AuthenticationManager authenticationManager,
            SecurityContextRepository securityContextRepository) {
        this.accounts = accounts;
        this.learners = learners;
        this.authenticationManager = authenticationManager;
        this.securityContextRepository = securityContextRepository;
    }

    record RegisterRequest(String email, String displayName, String password) {}

    record LoginRequest(String email, String password) {}

    record OnboardingRequest(String experience, Integer weeklyHours, String goal) {}

    record LearnerView(long id, String email, String displayName, boolean onboarded) {

        static LearnerView of(Learner learner) {
            return new LearnerView(learner.id(), learner.email(), learner.displayName(), learner.onboarded());
        }
    }

    /** {@code learner} is null when nobody is logged in. */
    record Me(LearnerView learner) {}

    @GetMapping("/auth/me")
    Me me(Authentication authentication) {
        return new Me(CurrentLearner.id(authentication).flatMap(learners::findById).map(LearnerView::of).orElse(null));
    }

    /** Issues the CSRF cookie; the frontend calls this once before its first state-changing request. */
    @GetMapping("/auth/csrf")
    void csrf(CsrfToken token) {
        token.getToken();
    }

    @PostMapping("/auth/register")
    Me register(@RequestBody RegisterRequest body, HttpServletRequest request, HttpServletResponse response) {
        accounts.register(body.email(), body.displayName(), body.password());
        return logIn(body.email(), body.password(), request, response);
    }

    @PostMapping("/auth/login")
    Me login(@RequestBody LoginRequest body, HttpServletRequest request, HttpServletResponse response) {
        return logIn(body.email(), body.password(), request, response);
    }

    @PostMapping("/onboarding")
    Me onboarding(@RequestBody OnboardingRequest body, Authentication authentication) {
        long learnerId = CurrentLearner.require(authentication);
        accounts.completeOnboarding(learnerId, body.experience(), body.weeklyHours(), body.goal());
        return new Me(learners.findById(learnerId).map(LearnerView::of).orElseThrow());
    }

    private Me logIn(String email, String password, HttpServletRequest request, HttpServletResponse response) {
        Authentication authentication = authenticationManager.authenticate(
                UsernamePasswordAuthenticationToken.unauthenticated(AccountService.normaliseEmail(email), password));
        // A new session id on login prevents session fixation.
        request.getSession(true);
        request.changeSessionId();
        SecurityContext context = SecurityContextHolder.createEmptyContext();
        context.setAuthentication(authentication);
        SecurityContextHolder.setContext(context);
        securityContextRepository.saveContext(context, request, response);
        return new Me(learners.findById(CurrentLearner.require(authentication)).map(LearnerView::of).orElseThrow());
    }
}
