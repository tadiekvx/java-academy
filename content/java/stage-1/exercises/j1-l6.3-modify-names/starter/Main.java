ArrayList<String> shout(ArrayList<String> names) {
    ArrayList<String> result = new ArrayList<>();
    for (String name : names) {
        result.add(name.toUpperCase());
    }
    return result;
}

void main() {
}
