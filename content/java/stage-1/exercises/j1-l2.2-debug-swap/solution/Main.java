void main() {
    String morning = "Coffee";
    String evening = "Tea";

    String saved = morning;
    morning = evening;
    evening = saved;

    IO.println(morning);
    IO.println(evening);
}
