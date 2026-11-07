String lastWeekday(String date) {
    LocalDate d = LocalDate.parse(date);
    LocalDate last = d.withDayOfMonth(d.lengthOfMonth());
        return last.toString();
}

void main() {
}
