int firstBreach(List<Integer> series, int threshold, int minutes) {
    int run = 0;
    for (int i = 0; i < series.size(); i++) {
        run = series.get(i) > threshold ? run + 1 : run;
        if (run >= minutes) {
            return i - minutes + 1;
        }
    }
    return -1;
}

void main() {
}
