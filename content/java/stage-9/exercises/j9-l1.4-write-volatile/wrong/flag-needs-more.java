String volatileEnough(String operation) {
    return switch (operation) {
        case "publish-immutable-object" -> "yes";
        case "stop-flag", "counter-increment", "check-then-act", "update-two-fields-together" -> "no";
        default -> "unknown";
    };
}

void main() {
}
