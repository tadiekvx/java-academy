String verifyToken(String token, String secret, long now) throws Exception {
    String[] parts = token.split("\\.", -1);
    if (parts.length != 3) {
        return "malformed";
    }
    String header;
    String payload;
    byte[] signature;
    try {
        header = new String(decode(parts[0]), java.nio.charset.StandardCharsets.UTF_8);
        payload = new String(decode(parts[1]), java.nio.charset.StandardCharsets.UTF_8);
    } catch (IllegalArgumentException e) {
        return "malformed";
    }
    if (!java.util.regex.Pattern.compile("\"alg\"\\s*:\\s*\"HS256\"").matcher(header).find()) {
        return "unsupported-alg";
    }
    try {
        signature = decode(parts[2]);
    } catch (IllegalArgumentException e) {
        return "malformed";
    }
    Mac mac = Mac.getInstance("HmacSHA256");
    mac.init(new SecretKeySpec(secret.getBytes(java.nio.charset.StandardCharsets.UTF_8), "HmacSHA256"));
    byte[] expected = mac.doFinal((parts[0] + "." + parts[1]).getBytes(java.nio.charset.StandardCharsets.UTF_8));
    if (!MessageDigest.isEqual(signature, expected)) {
        return "bad-signature";
    }
    java.util.regex.Matcher exp = java.util.regex.Pattern.compile("\"exp\"\\s*:\\s*(\\d+)").matcher(payload);
    if (!exp.find()) {
        return "malformed";
    }
    return now >= Long.parseLong(exp.group(1)) ? "expired" : "valid";
}

byte[] decode(String part) {
    if (!part.matches("[A-Za-z0-9_-]+")) {
        throw new IllegalArgumentException("not base64url");
    }
    return Base64.getUrlDecoder().decode(part);
}

void main() {
}
