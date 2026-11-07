List<String> subsets(String letters) {
    List<String> out = new ArrayList<>();
    collect(letters, 0, "", out);
    out.sort(Comparator.comparing(String::length).thenComparing(Comparator.naturalOrder()));
    return out;
}

void collect(String letters, int index, String chosen, List<String> out) {
    if (index == letters.length()) {
        out.add(chosen);
        return;
    }
    collect(letters, index + 1, chosen, out);
    collect(letters, index + 1, letters.charAt(index) + chosen, out);
}

void main() {
}
