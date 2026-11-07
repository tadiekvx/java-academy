void main() {
    int minutes = Integer.parseInt(IO.readln("Minutes parked: ").trim());
    int fee = minutes <= 30 ? 0 : Math.min((minutes - 30 + 59) / 60 * 2, 15);
    IO.println("Cost: " + fee);
}
