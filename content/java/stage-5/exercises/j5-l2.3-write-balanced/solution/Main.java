boolean balanced(String text) {
    Deque<Character> open = new ArrayDeque<>();
    for (char c : text.toCharArray()) {
        if (c == '(' || c == '[' || c == '{') {
            open.push(c);
        } else if (c == ')' || c == ']' || c == '}') {
            if (open.isEmpty()) {
                return false;
            }
            char top = open.pop();
            if ((c == ')' && top != '(') || (c == ']' && top != '[') || (c == '}' && top != '{')) {
                return false;
            }
        }
    }
    return open.isEmpty();
}

void main() {
}
