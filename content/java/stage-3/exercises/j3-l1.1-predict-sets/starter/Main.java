void main() {
    List<String> list = new ArrayList<>(List.of("b", "a", "b", "c"));
    Set<String> set = new HashSet<>(list);
    Set<String> sorted = new TreeSet<>(list);
    Set<String> ordered = new LinkedHashSet<>(list);
    IO.println(list.size());
    IO.println(set.size());
    IO.println(sorted);
    IO.println(ordered);
    IO.println(list.remove("b"));
    IO.println(list);
}
