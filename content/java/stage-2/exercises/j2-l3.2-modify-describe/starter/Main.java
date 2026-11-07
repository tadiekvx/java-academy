class Vehicle {
    String describe() {
        return "a vehicle";
    }
}

class Car extends Vehicle {
    @Override
    String describe() {
        return "a car";
    }
}

String describe(String kind) {
    Vehicle v;
    if (kind.equals("car")) {
        v = new Car();
    } else if (kind.equals("electric")) {
        v = new ElectricCar();
    } else {
        v = new Vehicle();
    }
    return v.describe();
}

void main() {
}
