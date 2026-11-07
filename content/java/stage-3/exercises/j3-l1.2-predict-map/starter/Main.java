void main() {
    Map<String, Integer> stock = new TreeMap<>();
    stock.put("apple", 3);
    stock.put("pear", 1);
    stock.put("apple", 5);
    stock.merge("pear", 2, Integer::sum);
    stock.putIfAbsent("fig", 9);
    stock.putIfAbsent("fig", 1);
    IO.println(stock);
    IO.println(stock.get("kiwi"));
    IO.println(stock.getOrDefault("kiwi", 0));
    IO.println(stock.containsKey("fig"));
    IO.println(stock.size());
}
