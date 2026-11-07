String volatileEnough(String operation) {
    return switch (operation) {
        case "stop-flag", "publish-immutable-object", "counter-increment" -> "yes";
        case "check-then-act", "update-two-fields-together" -> "no";
        default -> "unknown";
    };
}

void main() {
}
