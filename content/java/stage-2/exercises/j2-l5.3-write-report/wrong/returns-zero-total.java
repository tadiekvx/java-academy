int total(String[] items) {
    int sum = 0;
    for (String item : items) {
        sum += Integer.parseInt(item.trim());
    }
    return sum;
}

String report(String[] items) {
    try {
        return "total=" + total(items);
    } catch (NumberFormatException e) {
        return "total=0";
    }
}

void main() {
}
