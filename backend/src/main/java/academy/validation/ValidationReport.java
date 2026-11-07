package academy.validation;

import java.util.List;
import java.util.stream.Collectors;

import academy.content.Issue;

public record ValidationReport(List<Issue> issues) {

    public List<Issue> errors() {
        return issues.stream().filter(i -> i.severity() == Issue.Severity.ERROR).toList();
    }

    public List<Issue> warnings() {
        return issues.stream().filter(i -> i.severity() == Issue.Severity.WARNING).toList();
    }

    public String format() {
        if (issues.isEmpty()) {
            return "Content validation: no issues.";
        }
        return "Content validation: " + errors().size() + " error(s), " + warnings().size() + " warning(s)\n"
                + issues.stream()
                        .map(i -> "  " + i.severity() + "  " + i.location() + ": " + i.message().replace("\n", "\n      "))
                        .collect(Collectors.joining("\n"));
    }
}
