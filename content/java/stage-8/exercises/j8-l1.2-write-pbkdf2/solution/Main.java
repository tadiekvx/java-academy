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

void main() {
}
