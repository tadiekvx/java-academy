// INHERITED CODE: the staff model from the payroll system.

class Employee {
    String name;
    int base;

    Employee(String name, int base) {
        this.name = name;
        this.base = base;
    }

    int pay() {
        return base;
    }

    // Raise the base pay. (Written in a hurry.)
    Employee withRaise(int extra) {
        base += extra;
        return this;
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof Employee e)) {
            return false;
        }
        return name.equals(e.name) && base == e.base;
    }
}

class Manager extends Employee {
    int bonus;

    Manager(String name, int base, int bonus) {
        super(name, base);
        this.bonus = bonus;
    }

    @Override
    int pay() {
        return base + bonus;
    }

    @Override
    public boolean equals(Object other) {
        if (!(other instanceof Manager m)) {
            return false;
        }
        return super.equals(m) && bonus == m.bonus;
    }
}

// ---------------------------------------------------------------------------------------------
// The callers. Don't change them.
// ---------------------------------------------------------------------------------------------

String m1(String name, int base, int bonus) {
    Employee e = new Employee(name, base);
    Manager m = new Manager(name, base, bonus);
    return e.equals(m) + "," + m.equals(e) + "," + m.equals(new Manager(name, base, bonus)) + "," + m.equals(new Manager(name, base, bonus + 1));
}

String m2(String[] names, int[] bases, int[] bonuses) {
    Set<Employee> staff = new HashSet<>();
    for (int i = 0; i < names.length; i++) {
        staff.add(bonuses[i] < 0 ? new Employee(names[i], bases[i]) : new Manager(names[i], bases[i], bonuses[i]));
    }
    return String.valueOf(staff.size());
}

String m3(String name, int base, int bonus, int extra) {
    Employee original = bonus < 0 ? new Employee(name, base) : new Manager(name, base, bonus);
    Employee raised = original.withRaise(extra);
    return original.pay() + "->" + raised.pay();
}

void main() {
    // Optional: try the staff classes out here.
}
