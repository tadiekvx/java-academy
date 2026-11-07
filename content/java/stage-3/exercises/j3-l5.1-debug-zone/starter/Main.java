String nextDaySameTime(String local, String zone) {
    ZonedDateTime start = ZonedDateTime.of(LocalDateTime.parse(local), ZoneId.of(zone));
    ZonedDateTime next = start.plus(Duration.ofHours(24));
    return next.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));
}

void main() {
}
