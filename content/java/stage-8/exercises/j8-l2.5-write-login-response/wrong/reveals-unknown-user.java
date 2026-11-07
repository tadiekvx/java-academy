String loginResponse(boolean userExists, boolean passwordOk, boolean locked) {
    if (userExists && passwordOk && !locked) {
        return "200|ok";
    }
    if (!userExists) {
        return "401|No such user";
    }
    return "401|Invalid credentials";
}

void main() {
}
