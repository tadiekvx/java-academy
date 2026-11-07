import java.security.*;
import javax.crypto.*;
import javax.crypto.spec.*;

String hex(byte[] bytes) {
    StringBuilder out = new StringBuilder();
    for (byte b : bytes) {
        out.append(String.format("%02x", b));
    }
    return out.toString();
}

byte[] pbkdf2(String password, byte[] salt) throws Exception {
    PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 1000, 256);
    return SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
}

void main() throws Exception {
    byte[] saltA = {1, 2, 3, 4};
    byte[] saltB = {4, 3, 2, 1};
    String one = hex(pbkdf2("hunter2", saltA));
    String two = hex(pbkdf2("hunter2", saltA));
    String three = hex(pbkdf2("hunter2", saltB));
    String sha = hex(MessageDigest.getInstance("SHA-256").digest("abc".getBytes()));
    System.out.println("same password, same salt equal=" + one.equals(two));
    System.out.println("same password, other salt equal=" + one.equals(three));
    System.out.println("hash length=" + one.length());
    System.out.println("sha-256 of abc starts with " + sha.substring(0, 8));
}
