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
    FakeClock(int hour) {
    }

    public int hour() {
        return 9;
    }
}

String run(int hour) {
    return new Greeter().greet(new FakeClock(hour));
}

void main() {
}
