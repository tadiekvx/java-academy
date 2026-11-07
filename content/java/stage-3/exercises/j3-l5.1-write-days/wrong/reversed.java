long daysBetween(String from, String to) {
    return ChronoUnit.DAYS.between(LocalDate.parse(to), LocalDate.parse(from));
}

void main() {
}
