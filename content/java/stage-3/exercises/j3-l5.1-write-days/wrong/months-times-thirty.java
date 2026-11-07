long daysBetween(String from, String to) {
    LocalDate a = LocalDate.parse(from);
    LocalDate b = LocalDate.parse(to);
    return (b.getYear() - a.getYear()) * 365L + (b.getMonthValue() - a.getMonthValue()) * 30L + (b.getDayOfMonth() - a.getDayOfMonth());
}

void main() {
}
