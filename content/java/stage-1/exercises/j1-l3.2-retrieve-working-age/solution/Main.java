boolean isWorkingAge(int age) {
    return age >= 16 && age <= 66;
}

void main() {
    IO.println(isWorkingAge(30)); // should print true
}
