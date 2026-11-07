String compress(String text) {
    if (text.isEmpty()) {
        return "";
    }
    String result = "";
    char current = text.charAt(0);
    int run = 1;
    for (int i = 1; i < text.length(); i++) {
        if (text.charAt(i) == current) {
            run++;
        } else {
            result += current + "" + run;
            current = text.charAt(i);
            run = 1;
        }
    }
    result += current + "" + run;
    return result;
}

void main() {
}
