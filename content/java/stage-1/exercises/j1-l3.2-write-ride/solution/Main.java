boolean canRide(int heightCm, boolean withAdult) {
    return heightCm >= 120 || (heightCm >= 100 && withAdult);
}

void main() {
    IO.println(canRide(110, true)); // should print true
}
