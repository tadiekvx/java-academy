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
    int low = 0;
    int high = array.size() - 1;
    int found = -1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        int value = array.get(mid);
        if (value == target) {
            return mid;
        } else if (value < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return found;
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
