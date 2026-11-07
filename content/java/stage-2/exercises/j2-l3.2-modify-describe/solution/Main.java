class Vehicle {
    String describe() {
        return "a vehicle";
    }
}

class Car extends Vehicle {
    @Override
    String describe() {
        return super.describe() + " with 4 wheels";
    }
}

class ElectricCar extends Car {
    @Override
    String describe() {
        return super.describe() + " (electric)";
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
