int commonCount(List<String> a, List<String> b) {
    int n = 0;
    for (String s : a) {
        if (b.contains(s)) n++;
    }
    return n;
}

void main() {
}
