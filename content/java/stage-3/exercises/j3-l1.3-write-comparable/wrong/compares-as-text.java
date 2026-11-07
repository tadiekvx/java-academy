class Version implements Comparable<Version> {
    private final int major;
    private final int minor;

    Version(String text) {
        String[] parts = text.split("\\.");
        this.major = Integer.parseInt(parts[0]);
        this.minor = Integer.parseInt(parts[1]);
    }

    @Override
    public int compareTo(Version other) {
        return toString().compareTo(other.toString());
    }

    @Override
    public String toString() {
        return major + "." + minor;
    }
}

String newest(List<String> versions) {
    List<Version> list = new ArrayList<>();
    for (String v : versions) {
        list.add(new Version(v));
    }
    return Collections.max(list).toString();
}

void main() {
}
