List<Integer> split(int totalPence, int people) {
    List<Integer> shares = new ArrayList<>();
    for (int i = 0; i < people; i++) {
        shares.add(totalPence / people + (i < totalPence % people ? 1 : 0));
    }
    return shares;
}

void main() {
}
