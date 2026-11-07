int countFields(String line) {
    int n = 0;
    for (char c : line.toCharArray()) {
        if (c == ',') n++;
    }
    return n;
}

void main() {
}
