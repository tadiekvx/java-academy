String pbkdf2Hex(String password, String saltHex, int iterations) throws Exception {
    byte[] salt = new byte[saltHex.length() / 2];
    for (int i = 0; i < salt.length; i++) {
        salt[i] = (byte) Integer.parseInt(saltHex.substring(2 * i, 2 * i + 2), 16);
    }
    MessageDigest digest = MessageDigest.getInstance("SHA-256");
    digest.update(salt);
    byte[] key = digest.digest(password.getBytes(java.nio.charset.StandardCharsets.UTF_8));
    StringBuilder hex = new StringBuilder();
    for (byte b : key) {
        hex.append(String.format("%02x", b));
    }
    return hex.toString();
}

void main() {
}
