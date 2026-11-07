List<String> sagaTrace(List<String> steps, int failAt) {
    List<String> trace = new ArrayList<>();
    for (int i = 0; i < steps.size(); i++) {
        if (i == failAt) {
            trace.add("fail:" + steps.get(i));
            for (int done = i - 1; done >= 0; done--) {
                trace.add("undo:" + steps.get(done));
            }
        }
        trace.add("do:" + steps.get(i));
    }
    return trace;
}

void main() {
}
