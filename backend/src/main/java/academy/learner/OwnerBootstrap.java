package academy.learner;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

/**
 * Creates the single owner account on a server where public registration is closed. Runs only when
 * ACADEMY_OWNER_EMAIL and ACADEMY_OWNER_PASSWORD are set, and never changes an existing account.
 */
@Component
class OwnerBootstrap implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(OwnerBootstrap.class);

    private final AccountService accounts;
    private final LearnerRepository learners;
    private final String email;
    private final String password;
    private final String displayName;

    OwnerBootstrap(AccountService accounts, LearnerRepository learners,
            @Value("${academy.owner.email:}") String email,
            @Value("${academy.owner.password:}") String password,
            @Value("${academy.owner.display-name:Owner}") String displayName) {
        this.accounts = accounts;
        this.learners = learners;
        this.email = email;
        this.password = password;
        this.displayName = displayName;
    }

    @Override
    public void run(ApplicationArguments args) {
        if (email.isBlank() || password.isBlank()) {
            return;
        }
        if (learners.emailExists(AccountService.normaliseEmail(email))) {
            return;
        }
        accounts.register(email, displayName, password);
        log.info("Created the owner account for {}", AccountService.normaliseEmail(email));
    }
}
