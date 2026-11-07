class Version {
    private final int major;
    private final int minor;

    Version(int major, int minor) {
        this.major = major;
        this.minor = minor;
    }

    Version bumpMinor() {
        return new Version(major, minor + 1);
    }

    Version bumpMajor() {
        return new Version(major + 1, minor);
    }

    @Override
    public String toString() {
        return major + "." + minor;
    }
}

String run(int major, int minor, String[] ops) {
    Version original = new Version(major, minor);
    Version current = original;
    for (String op : ops) {
        current = op.equals("major") ? current.bumpMajor() : current.bumpMinor();
    }
    return current + " (was " + original + ")";
}

void main() {
}
