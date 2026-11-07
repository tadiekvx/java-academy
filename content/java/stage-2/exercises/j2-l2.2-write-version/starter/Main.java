class Version {
    private int major;
    private int minor;

    Version(int major, int minor) {
        this.major = major;
        this.minor = minor;
    }

    Version bumpMinor() {
        minor++;
        return this;
    }

    Version bumpMajor() {
        major++;
        minor = 0;
        return this;
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
