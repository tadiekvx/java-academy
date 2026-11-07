String windDescription(int mph) {
    if (mph < 1) {
        return "Calm";
    } else if (mph < 13) {
        return "Breeze";
    } else if (mph < 39) {
        return "Windy";
    } else {
        return "Gale";
    }
}

void main() {
    IO.println(windDescription(20)); // should print Windy
}
