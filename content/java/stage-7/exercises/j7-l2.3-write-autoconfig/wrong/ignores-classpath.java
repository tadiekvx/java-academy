List<String> autoConfigure(List<String> classpath, List<String> userBeans) {
    String[][] rules = {{"webmvc", "DispatcherServlet"}, {"jackson", "ObjectMapper"}, {"jdbc", "DataSource"}};
    List<String> created = new ArrayList<>();
    for (String[] rule : rules) {
        if (!userBeans.contains(rule[1])) {
            created.add(rule[1]);
        }
    }
    Collections.sort(created);
    return created;
}

void main() {
}
