String loginResponse(boolean userExists, boolean passwordOk, boolean locked) {
    if (userExists && passwordOk && !locked) {
        return "200|ok";
    }
    return "401|Invalid credentials";
}

void main() {
}
