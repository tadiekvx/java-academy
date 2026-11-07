String loginResponse(boolean userExists, boolean passwordOk, boolean locked) {
    if (userExists && passwordOk && !locked) {
        return "200|ok";
    }
    if (locked) {
        return "423|Account locked";
    }
    return "401|Invalid credentials";
}

void main() {
}
