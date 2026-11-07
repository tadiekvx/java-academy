package academy.api;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/** Serves the single-page frontend's index for its client-side routes, so deep links and reloads work. */
@Controller
class FrontendController {

    @GetMapping({"/", "/lessons", "/lessons/{id}", "/signup", "/login", "/welcome", "/checks/{id}", "/projects", "/projects/{id}"})
    String index() {
        return "forward:/index.html";
    }
}
