String safeDivide(String a, String b) {
    try {
        int x = Integer.parseInt(a.trim());
        int y = Integer.parseInt(b.trim());
        return String.valueOf(x / y);
    } catch (NumberFormatException e) {
        return "divide by zero";
    } catch (ArithmeticException e) {
        return "not a number";
    }
}

void main() {
}
