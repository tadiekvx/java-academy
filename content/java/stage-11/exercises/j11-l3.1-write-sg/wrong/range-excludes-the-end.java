boolean sgAllows(List<String> rules, String protocol, int port, String ip) {
    long address = toInt(ip);
    if (address < 0) {
        return false;
    }
    for (String rule : rules) {
        String[] p = rule.split(":");
        if (!p[0].equals(protocol)) {
            continue;
        }
        String[] range = p[1].split("-");
        int low = Integer.parseInt(range[0]);
        int high = Integer.parseInt(range[range.length - 1]);
        String[] cidr = p[2].split("/");
        int bits = Integer.parseInt(cidr[1]);
        long mask = bits == 0 ? 0 : (0xFFFFFFFFL << (32 - bits)) & 0xFFFFFFFFL;
        if (port >= low && port < high && (address & mask) == (toInt(cidr[0]) & mask)) {
            return true;
        }
    }
    return false;
}

long toInt(String ip) {
    String[] parts = ip.split("\\.");
    if (parts.length != 4) {
        return -1;
    }
    long value = 0;
    for (String part : parts) {
        int octet;
        try {
            octet = Integer.parseInt(part);
        } catch (NumberFormatException e) {
            return -1;
        }
        if (octet < 0 || octet > 255) {
            return -1;
        }
        value = value * 256 + octet;
    }
    return value;
}

void main() {
}
