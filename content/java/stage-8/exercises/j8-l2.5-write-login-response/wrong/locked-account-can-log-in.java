String loginResponse(boolean userExists, boolean passwordOk, boolean locked) {
    if (userExists && passwordOk) {
        return "200|ok";
    }
    return "401|Invalid credentials";
}

void main() {
}
