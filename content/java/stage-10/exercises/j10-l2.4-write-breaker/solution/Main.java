List<String> breakerOutcomes(List<String> results, int threshold, int cooldown) {
    List<String> out = new ArrayList<>();
    String state = "closed";
    int failures = 0;
    int remaining = 0;
    for (String result : results) {
        if (state.equals("open")) {
            out.add("rejected");
            remaining--;
            if (remaining == 0) {
                state = "half";
            }
            continue;
        }
        if (result.equals("ok")) {
            out.add("ok");
            state = "closed";
            failures = 0;
        } else {
            out.add("fail");
            if (state.equals("half")) {
                state = "open";
                remaining = cooldown;
            } else {
                failures++;
                if (failures >= threshold) {
                    state = "open";
                    remaining = cooldown;
                }
            }
        }
        if (state.equals("open") && remaining == 0) {
            state = "half";
        }
    }
    return out;
}

void main() {
}
