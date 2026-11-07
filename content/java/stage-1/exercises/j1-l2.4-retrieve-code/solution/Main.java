String shortCode(String city) {
    return city.substring(0, 3).toUpperCase();
}

void main() {
    IO.println(shortCode("London")); // should print LON
}
