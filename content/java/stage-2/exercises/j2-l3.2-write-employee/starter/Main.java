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

// Write the classes Manager and Engineer here.

int payFor(String role, int base) {
    Employee e = role.equals("manager") ? new Manager("M", base) : new Engineer("E", base);
    return e.pay();
}

void main() {
}
