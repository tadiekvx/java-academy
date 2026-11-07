String windDescription(int mph) {
    if (mph < 39) {
        return "Windy";
    } else if (mph < 13) {
        return "Breeze";
    } else if (mph < 1) {
        return "Calm";
    } else {
        return "Gale";
    }
}

void main() {
}
