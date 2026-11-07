String volatileEnough(String operation) {
    return switch (operation) {
        case "stop-flag", "publish-immutable-object" -> "yes";
        case "counter-increment", "check-then-act", "update-two-fields-together" -> "yes";
        default -> "unknown";
    };
}

void main() {
}
