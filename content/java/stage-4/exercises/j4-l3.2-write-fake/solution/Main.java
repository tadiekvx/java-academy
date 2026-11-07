interface Clock {
    int hour();
}

class Greeter {
    String greet(Clock clock) {
        int hour = clock.hour();
        return hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
    }
}

class FakeClock implements Clock {
    private final int hour;

    FakeClock(int hour) {
        this.hour = hour;
    }

    public int hour() {
        return hour;
    }
}

String run(int hour) {
    return new Greeter().greet(new FakeClock(hour));
}

void main() {
}
