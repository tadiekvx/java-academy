String pbkdf2Hex(String password, String saltHex, int iterations) throws Exception {
    byte[] salt = new byte[saltHex.length() / 2];
    for (int i = 0; i < salt.length; i++) {
        salt[i] = (byte) Integer.parseInt(saltHex.substring(2 * i, 2 * i + 2), 16);
    }
    PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, iterations, 256);
    byte[] key = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
    StringBuilder hex = new StringBuilder();
    for (byte b : key) {
        hex.append(String.format("%02x", b));
    }
    return hex.toString();
}

String verify(String attempt, String saltHex, int iterations, String expectedHex) throws Exception {
    byte[] got = pbkdf2Hex(attempt, saltHex, iterations).getBytes(java.nio.charset.StandardCharsets.UTF_8);
    byte[] want = expectedHex.getBytes(java.nio.charset.StandardCharsets.UTF_8);
    return new String(got).equals(new String(want)) ? "true" : "false";
}

void main() {
}
