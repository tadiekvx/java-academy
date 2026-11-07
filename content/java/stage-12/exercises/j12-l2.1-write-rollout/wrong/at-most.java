boolean inRollout(String user, String flag, int percent) {
    java.util.zip.CRC32 crc = new java.util.zip.CRC32();
    crc.update((flag + ":" + user).getBytes(java.nio.charset.StandardCharsets.UTF_8));
    return crc.getValue() % 100 <= percent;
}

void main() {
}
