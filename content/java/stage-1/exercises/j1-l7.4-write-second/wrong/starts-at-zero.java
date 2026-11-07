int secondLargest(int[] values) {
    int largest = 0, second = 0;
    boolean any = false;
    for (int v : values) {
        if (v > largest) { second = largest; largest = v; any = true; }
        else if (v < largest && v > second) { second = v; any = true; }
    }
    return any && second != 0 ? second : -1;
}

void main() {
}
