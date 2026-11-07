package academy.learner;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

/**
 * Loads learners for login by email. The authenticated principal's name is the learner's id, so
 * the rest of the platform never depends on the (changeable) email address.
 */
@Service
class LearnerDetailsService implements UserDetailsService {

    private final LearnerRepository learners;

    LearnerDetailsService(LearnerRepository learners) {
        this.learners = learners;
    }

    @Override
    public UserDetails loadUserByUsername(String email) {
        return learners.findCredentials(AccountService.normaliseEmail(email))
                .map(c -> User.withUsername(Long.toString(c.id())).password(c.passwordHash()).roles("LEARNER").build())
                .orElseThrow(() -> new UsernameNotFoundException("No learner with that email"));
    }
}
