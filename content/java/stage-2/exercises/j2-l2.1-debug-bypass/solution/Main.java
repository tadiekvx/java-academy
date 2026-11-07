class Thermostat {
    private int target = 20;

    void setTarget(int t) {
        if (t < 10 || t > 30) {
            return;
        }
        target = t;
    }

    int target() {
        return target;
    }
}

int run(int[] values) {
    Thermostat th = new Thermostat();
    for (int v : values) {
        th.setTarget(v);
    }
    return th.target();
}

void main() {
}
