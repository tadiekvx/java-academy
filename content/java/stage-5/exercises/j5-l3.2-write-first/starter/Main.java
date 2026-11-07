class CountingArray {
    private final int[] data;
    int reads;

    CountingArray(int[] data) {
        this.data = data;
    }

    int size() {
        return data.length;
    }

    int get(int index) {
        reads++;
        return data[index];
    }
}

int firstIndex(CountingArray array, int target) {
    for (int i = 0; i < array.size(); i++) {
        if (array.get(i) == target) {
            return i;
        }
    }
    return -1;
}

String run(int n, int target) {
    int[] data = new int[n];
    for (int i = 0; i < n; i++) {
        data[i] = i / 3;
    }
    CountingArray array = new CountingArray(data);
    int index = firstIndex(array, target);
    int limit = 2 * (32 - Integer.numberOfLeadingZeros(Math.max(n, 1))) + 4;
    return index + " fast=" + (array.reads <= limit);
}

void main() {
}
