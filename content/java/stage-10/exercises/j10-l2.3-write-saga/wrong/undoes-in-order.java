List<String> sagaTrace(List<String> steps, int failAt) {
    List<String> trace = new ArrayList<>();
    for (int i = 0; i < steps.size(); i++) {
        if (i == failAt) {
            trace.add("fail:" + steps.get(i));
            for (int done = 0; done < i; done++) {
                trace.add("undo:" + steps.get(done));
            }
            return trace;
        }
        trace.add("do:" + steps.get(i));
    }
    return trace;
}

void main() {
}
