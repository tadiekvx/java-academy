List<String> rank(List<String> threats) {
    List<String[]> rows = new ArrayList<>();
    for (String threat : threats) {
        String[] p = threat.split(":");
        rows.add(new String[] {p[0], String.valueOf(Integer.parseInt(p[1]) * Integer.parseInt(p[2]))});
    }
    rows.sort((a, b) -> {
        int byScore = Integer.compare(Integer.parseInt(b[1]), Integer.parseInt(a[1]));
        return byScore;
    });
    List<String> out = new ArrayList<>();
    for (String[] row : rows) {
        out.add(row[0] + "=" + row[1]);
    }
    return out;
}

void main() {
}
