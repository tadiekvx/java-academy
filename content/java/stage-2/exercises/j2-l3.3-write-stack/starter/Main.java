class Stack extends ArrayList<Integer> {
}

String run(String[] ops) {
    Stack s = new Stack();
    StringBuilder out = new StringBuilder();
    for (String op : ops) {
        if (op.startsWith("push:")) {
            s.push(Integer.parseInt(op.substring(5)));
        } else if (op.equals("pop")) {
            out.append(out.isEmpty() ? "" : ",").append(s.pop());
        } else if (op.equals("peek")) {
            out.append(out.isEmpty() ? "" : ",").append(s.peek());
        }
    }
    return out + "|" + s.size();
}

void main() {
}
