String sentence(List<String> items) {
    if (items.isEmpty()) {
        return "nothing";
    }
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < items.size(); i++) {
        if (i > 0) {
            sb.append(", ");
        }
        sb.append(items.get(i));
    }
    return sb.toString();
}

void main() {
}
