Function<Integer, Integer> stepFor(String name) {
    return x -> x;
}

int applySteps(String steps, int start) {
    Function<Integer, Integer> all = x -> x;
    if (!steps.isEmpty()) {
        for (String name : steps.split(",")) {
            all = all.andThen(stepFor(name));
        }
    }
    return all.apply(start);
}

void main() {
}
