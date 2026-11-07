void main() {
    String[] keys = {"Aa", "BB", "pear", "fig", "apple"};
    for (String key : keys) {
        IO.println(key + " " + key.hashCode() + " " + Math.floorMod(key.hashCode(), 8));
    }
    for (int i = 0; i < 3; i++) {
        IO.println(keys[i] + " " + Math.floorMod(keys[i].hashCode(), 16));
    }
}
