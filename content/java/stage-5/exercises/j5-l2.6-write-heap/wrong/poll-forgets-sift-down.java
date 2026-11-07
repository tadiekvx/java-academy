class MinHeap {
    private int[] data = new int[4];
    private int size;

    void add(int value) {
        if (size == data.length) {
            data = Arrays.copyOf(data, data.length * 2);
        }
        data[size] = value;
        int i = size;
        size++;
        while (i > 0 && data[i] < data[(i - 1) / 2]) {
            swap(i, (i - 1) / 2);
            i = (i - 1) / 2;
        }
    }

    int poll() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        int min = data[0];
        size--;
        data[0] = data[size];
        int i = 0;
        while (true) {
            int left = 2 * i + 1;
            int right = 2 * i + 2;
            int smallest = i;
            if (left < size && data[left] < data[smallest]) {
                smallest = left;
            }
            if (right < size && data[right] < data[smallest]) {
                smallest = right;
            }
            if (smallest == i) {
                break;
            }
            break;
        }
        return min;
    }

    int peek() {
        if (size == 0) {
            throw new NoSuchElementException();
        }
        return data[0];
    }

    int size() {
        return size;
    }

    private void swap(int a, int b) {
        int t = data[a];
        data[a] = data[b];
        data[b] = t;
    }
}

void main() {
}
