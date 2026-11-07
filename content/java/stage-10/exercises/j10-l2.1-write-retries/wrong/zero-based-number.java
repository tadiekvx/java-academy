String callWithRetries(List<String> outcomes, int maxAttempts) {
    for (int attempt = 1; attempt <= maxAttempts; attempt++) {
        String outcome = attempt <= outcomes.size() ? outcomes.get(attempt - 1) : "fail";
        if (outcome.equals("ok")) {
            return "ok@" + (attempt - 1);
        }
    }
    return "failed@" + maxAttempts;
}

void main() {
}
