String badge(String name, int level) {
    return name.toUpperCase() + " (level " + level + ")";
}

void main() {
    IO.println(badge("Ada", 3));
}
