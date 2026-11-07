String lastWeekday(String date) {
    LocalDate d = LocalDate.parse(date);
    LocalDate last = d.withDayOfMonth(d.lengthOfMonth());
    while (last.getDayOfWeek() == DayOfWeek.SATURDAY || last.getDayOfWeek() == DayOfWeek.SUNDAY) {
        last = last.minusDays(1);
    }
    return last.toString();
}

void main() {
}
