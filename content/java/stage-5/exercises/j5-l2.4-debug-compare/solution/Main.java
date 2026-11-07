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
        return Math.floorMod(key.hashCode(), capacity);
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
                int i = indexFor(e.key, buckets.length);
                buckets[i] = new Entry(e.key, e.value, buckets[i]);
            }
        }
    }
}

String run(String[] ops) {
    StringIntMap map = new StringIntMap();
    StringBuilder out = new StringBuilder();
    for (String op : ops) {
        if (op.startsWith("put:")) {
            String[] kv = op.substring(4).split("=");
            map.put(kv[0], Integer.parseInt(kv[1]));
        } else if (op.startsWith("get:")) {
            out.append(map.getOrDefault(op.substring(4), -1)).append(" ");
        } else if (op.startsWith("remove:")) {
            out.append(map.remove(op.substring(7)) ? "T" : "F").append(" ");
        }
    }
    return out + "size=" + map.size();
}

void main() {
}
