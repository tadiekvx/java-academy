boolean isTeenager(int age) {
    return age >= 13 && age <= 19;
}

void main() {
    IO.println(isTeenager(15)); // should print true
}
