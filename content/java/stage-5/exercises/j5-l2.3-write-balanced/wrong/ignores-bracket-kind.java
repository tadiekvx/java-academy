boolean balanced(String text) {
    int depth = 0;
    for (char c : text.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') depth++;
        else if (c == ')' || c == ']' || c == '}') {
            depth--;
            if (depth < 0) return false;
        }
    }
    return depth == 0;
}

void main() {
}
