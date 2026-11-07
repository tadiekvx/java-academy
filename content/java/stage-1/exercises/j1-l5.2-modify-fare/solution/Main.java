int distanceCost(int miles) {
    return miles * 150;
}

int bookingFee() {
    return 300;
}

int fare(int miles) {
    int total = bookingFee() + distanceCost(miles);
    if (miles > 10) {
        total += 200;
    }
    return total;
}

void main() {
    IO.println(fare(4));
}
