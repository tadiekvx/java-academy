class IntBst {
    void insert(int value) {
    }

    boolean contains(int value) {
        return false;
    }

    int size() {
        return 0;
    }

    int height() {
        return 0;
    }

    List<Integer> inOrder() {
        return new ArrayList<>();
    }
}

String run(int[] values, int probe) {
    IntBst tree = new IntBst();
    for (int v : values) {
        tree.insert(v);
    }
    return "inorder=" + tree.inOrder() + " size=" + tree.size() + " height=" + tree.height() + " contains=" + tree.contains(probe);
}

void main() {
}
