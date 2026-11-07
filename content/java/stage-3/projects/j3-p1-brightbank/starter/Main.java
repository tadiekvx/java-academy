// Brightbank v3: read a bank's CSV export. Each line is  date,description,amount  (amount in pounds, e.g. -2.50).
// Money.format is given. The methods below compile but return wrong answers. The brief says what each must do.

class Money {
    static String format(int pence) {
        String sign = pence < 0 ? "-" : "";
        int absolute = Math.abs(pence);
        String padding = absolute % 100 < 10 ? "0" : "";
        return sign + "£" + absolute / 100 + "." + padding + absolute % 100;
    }
}

String summary(List<String> lines) {
    return "";
}

String monthlyTotals(List<String> lines) {
    return "";
}

String statement(List<String> lines, String from, String to) {
    return "";
}

String uniqueSummary(List<String> lines) {
    return "";
}

void main() {
    // Optional: try your methods out here.
}
