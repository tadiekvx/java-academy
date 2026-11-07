long copiesWhenAdding(int n) {
    long capacity = 4;
    long copies = 0;
    while (n >= capacity) {
        copies += capacity;
        capacity *= 2;
    }
    return copies;
}

void main() {
}
