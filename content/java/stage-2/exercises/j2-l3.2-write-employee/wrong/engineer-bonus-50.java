abstract class Employee {
    String name;
    int base;

    Employee(String name, int base) {
        this.name = name;
        this.base = base;
    }

    abstract int bonus();

    int pay() {
        return base + bonus();
    }
}

class Manager extends Employee {
    Manager(String name, int base) {
        super(name, base);
    }

    int bonus() {
        return base / 10;
    }
}

class Engineer extends Employee {
    Engineer(String name, int base) {
        super(name, base);
    }

    int bonus() {
        return 50;
    }
}

int payFor(String role, int base) {
    Employee e = role.equals("manager") ? new Manager("M", base) : new Engineer("E", base);
    return e.pay();
}

void main() {
}
