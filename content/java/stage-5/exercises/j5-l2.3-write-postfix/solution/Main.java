int evalPostfix(String expr) {
    Deque<Integer> stack = new ArrayDeque<>();
    for (String token : expr.split(" ")) {
        switch (token) {
            case "+" -> stack.push(stack.pop() + stack.pop());
            case "*" -> stack.push(stack.pop() * stack.pop());
            case "-" -> {
                int right = stack.pop();
                stack.push(stack.pop() - right);
            }
            case "/" -> {
                int right = stack.pop();
                stack.push(stack.pop() / right);
            }
            default -> stack.push(Integer.parseInt(token));
        }
    }
    return stack.pop();
}

void main() {
}
