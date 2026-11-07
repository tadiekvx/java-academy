String toStatus(String exception) {
    return switch (exception) {
        case "IllegalArgumentException" -> "400|Bad Request";
        case "EmailTakenException" -> "400|Bad Request";
        case "MentorUnavailableException" -> "503|Service Unavailable";
        case "AuthenticationException" -> "401|Unauthorized";
        default -> "500|Internal Server Error";
    };
}

void main() {
}
