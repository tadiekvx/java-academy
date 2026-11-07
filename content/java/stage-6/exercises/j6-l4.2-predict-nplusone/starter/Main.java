import java.util.*;

class Store {
    int queries = 0;
    final Map<String, List<String>> accountsByCustomer = new LinkedHashMap<>();

    Store() {
        accountsByCustomer.put("Ada Lovelace", List.of("1200.00", "50.00"));
        accountsByCustomer.put("Grace Hopper", List.of("300.50"));
        accountsByCustomer.put("Alan Turing", List.of());
        accountsByCustomer.put("Edsger Dijkstra", List.of("780.25"));
    }

    List<String> loadCustomers() {
        queries++;
        return new ArrayList<>(accountsByCustomer.keySet());
    }

    List<String> loadAccounts(String customer) {
        queries++;
        return accountsByCustomer.get(customer);
    }

    Map<String, List<String>> loadCustomersWithAccounts() {
        queries++;
        return accountsByCustomer;
    }
}

void main() {
    Store lazy = new Store();
    List<String> lazyLines = new ArrayList<>();
    for (String customer : lazy.loadCustomers()) {
        lazyLines.add(customer + " " + lazy.loadAccounts(customer));
    }
    System.out.println("lazy queries=" + lazy.queries);

    Store fetched = new Store();
    List<String> fetchedLines = new ArrayList<>();
    for (var entry : fetched.loadCustomersWithAccounts().entrySet()) {
        fetchedLines.add(entry.getKey() + " " + entry.getValue());
    }
    System.out.println("join fetch queries=" + fetched.queries);
    System.out.println("same report=" + lazyLines.equals(fetchedLines));
}
