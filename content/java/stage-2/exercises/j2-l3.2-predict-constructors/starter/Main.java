class Vehicle {
    Vehicle() {
        IO.println("Vehicle built");
    }

    String describe() {
        return "a vehicle";
    }
}

class Car extends Vehicle {
    Car() {
        IO.println("Car built");
    }

    @Override
    String describe() {
        return super.describe() + " with 4 wheels";
    }
}

void main() {
    Vehicle v = new Car();
    IO.println(v.describe());
}
