List<String> visibleAccounts(String user, String role, List<String> accounts) {
    List<String> ids = new ArrayList<>();
    for (String account : accounts) {
        ids.add(account.split(":")[0]);
    }
    return ids;
}

void main() {
}
