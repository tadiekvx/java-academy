String label(int temperature) {
    String result = "Mild";
    if (temperature > 25); {
        result = "Hot";
    }
    return result;
}

void main() {
    IO.println(label(10)); // should print Mild
}
