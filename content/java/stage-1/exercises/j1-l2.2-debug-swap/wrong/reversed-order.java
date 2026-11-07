void main() {
    String morning = "Coffee";
    String evening = "Tea";

    evening = morning;
    morning = evening;

    IO.println(morning);
    IO.println(evening);
}
