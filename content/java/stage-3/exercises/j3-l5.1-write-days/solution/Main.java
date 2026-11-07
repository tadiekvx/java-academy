long daysBetween(String from, String to) {
    return ChronoUnit.DAYS.between(LocalDate.parse(from), LocalDate.parse(to));
}

void main() {
}
