class StringIntMap {
    private static class Entry {
        final String key;
        int value;
        Entry next;

        Entry(String key, int value, Entry next) {
            this.key = key;
            this.value = value;
            this.next = next;
        }
    }

    private Entry[] buckets = new Entry[8];
    private int size;

    private int indexFor(String key, int capacity) {
        return Math.abs(key.hashCode() % capacity);
    }

    void put(String key, int value) {
        int i = indexFor(key, buckets.length);
        for (Entry e = buckets[i]; e != null; e = e.next) {
            if (e.key.equals(key)) {
                e.value = value;
                return;
            }
        }
        buckets[i] = new Entry(key, value, buckets[i]);
        size++;
        if (size > buckets.length * 3 / 4) {
            resize();
        }
    }

    int getOrDefault(String key, int fallback) {
        for (Entry e = buckets[indexFor(key, buckets.length)]; e != null; e = e.next) {
            if (e.key.equals(key)) {
                return e.value;
            }
        }
        return fallback;
    }

    boolean remove(String key) {
        int i = indexFor(key, buckets.length);
        Entry previous = null;
        for (Entry e = buckets[i]; e != null; e = e.next) {
            if (e.key.equals(key)) {
                if (previous == null) {
                    buckets[i] = e.next;
                } else {
                    previous.next = e.next;
                }
                size--;
                return true;
            }
            previous = e;
        }
        return false;
    }

    int size() {
        return size;
    }

    private void resize() {
        Entry[] old = buckets;
        buckets = new Entry[old.length * 2];
        for (Entry head : old) {
            for (Entry e = head; e != null; e = e.next) {
                int i = indexFor(e.key, old.length) % buckets.length;
                buckets[i] = new Entry(e.key, e.value, buckets[i]);
            }
        }
    }
}

void main() {
}
