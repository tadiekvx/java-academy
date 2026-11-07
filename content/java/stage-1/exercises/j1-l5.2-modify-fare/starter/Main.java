int distanceCost(int miles) {
    return miles * 150;
}

int bookingFee() {
    return 300;
}

int fare(int miles) {
    return bookingFee() + distanceCost(miles);
}

void main() {
    IO.println(fare(4));
}
