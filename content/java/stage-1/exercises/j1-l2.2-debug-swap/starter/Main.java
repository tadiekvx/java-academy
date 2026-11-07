void main() {
    String morning = "Coffee";
    String evening = "Tea";

    morning = evening;
    evening = morning;

    IO.println(morning);
    IO.println(evening);
}
