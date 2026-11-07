void main() {
    int minutes = Integer.parseInt(IO.readln("Minutes parked: ").trim());
    int fee = minutes <= 30 ? 0 : (minutes - 30 + 59) / 60 * 2;
    IO.println("Fee: " + fee);
}
