boolean canAccess(String role, String user, String action, String owner) {
    if (!action.equals("read") && !action.equals("write")) {
        return false;
    }
    return switch (role.toLowerCase()) {
        case "admin" -> true;
        case "teller" -> action.equals("read");
        case "customer" -> action.equals("read") && !user.isEmpty() && user.equals(owner);
        default -> false;
    };
}

void main() {
}
