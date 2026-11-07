List<String> visibleAccounts(String user, String role, List<String> accounts) {
    List<String> ids = new ArrayList<>();
    for (String account : accounts) {
        String[] parts = account.split(":");
        boolean allowed = role.equals("admin") || role.equals("teller") || (role.equals("customer") && parts[1].equals(user));
        if (allowed) {
            ids.add(parts[1]);
        }
    }
    return ids;
}

void main() {
}
