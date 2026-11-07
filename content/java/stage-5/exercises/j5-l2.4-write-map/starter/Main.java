class StringIntMap {
    void put(String key, int value) {
    }

    int getOrDefault(String key, int fallback) {
        return fallback;
    }

    boolean remove(String key) {
        return false;
    }

    int size() {
        return 0;
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
