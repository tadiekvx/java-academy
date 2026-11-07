int attempt(String s) {
    try {
        IO.println("parsing");
        int n = Integer.parseInt(s);
        IO.println("parsed " + n);
        return n;
    } catch (NumberFormatException e) {
        IO.println("bad");
        return -1;
    } finally {
        IO.println("done");
    }
}

void main() {
    IO.println(attempt("12"));
    IO.println(attempt("x"));
}
