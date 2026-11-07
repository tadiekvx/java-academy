long copiesWhenAdding(int n) {
    long copies = 0;
    for (long size = 4; size < n; size++) {
        copies += size;
    }
    return copies;
}

void main() {
}
