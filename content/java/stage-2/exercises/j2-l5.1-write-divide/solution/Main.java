String safeDivide(String a, String b) {
    try {
        int x = Integer.parseInt(a.trim());
        int y = Integer.parseInt(b.trim());
        return String.valueOf(x / y);
    } catch (NumberFormatException e) {
        return "not a number";
    } catch (ArithmeticException e) {
        return "divide by zero";
    }
}

void main() {
}
