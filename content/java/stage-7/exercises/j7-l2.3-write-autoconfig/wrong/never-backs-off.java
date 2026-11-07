List<String> autoConfigure(List<String> classpath, List<String> userBeans) {
    String[][] rules = {{"webmvc", "DispatcherServlet"}, {"jackson", "ObjectMapper"}, {"jdbc", "DataSource"}};
    List<String> created = new ArrayList<>();
    for (String[] rule : rules) {
        if (classpath.contains(rule[0])) {
            created.add(rule[1]);
        }
    }
    Collections.sort(created);
    return created;
}

void main() {
}
