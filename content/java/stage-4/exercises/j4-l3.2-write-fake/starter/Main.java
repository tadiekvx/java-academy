interface Clock {
    int hour();
}

class Greeter {
    String greet(Clock clock) {
        int hour = clock.hour();
        return hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";
    }
}

// Write the class FakeClock here.

String run(int hour) {
    return new Greeter().greet(new FakeClock(hour));
}

void main() {
}
