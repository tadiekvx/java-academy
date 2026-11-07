int secondLargest(int[] values) {
    boolean haveLargest = false;
    boolean haveSecond = false;
    int largest = 0;
    int second = 0;
    for (int value : values) {
        if (!haveLargest || value > largest) {
            if (haveLargest) {
                second = largest;
                haveSecond = true;
            }
            largest = value;
            haveLargest = true;
        } else if (value < largest && (!haveSecond || value > second)) {
            second = value;
            haveSecond = true;
        }
    }
    return haveSecond ? second : -1;
}

void main() {
}
