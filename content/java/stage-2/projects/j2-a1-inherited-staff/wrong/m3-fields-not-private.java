class Employee {
    final String name;
    final int base;

    Employee(String name, int base) {
        this.name = name;
        this.base = base;
    }

    String name() {
        return name;
    }

    int base() {
        return base;
    }

    int pay() {
        return base;
    }

    Employee withRaise(int extra) {
        return new Employee(name, base + extra);
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }
        if (other == null || getClass() != other.getClass()) {
            return false;
        }
        Employee e = (Employee) other;
        return name.equals(e.name) && base == e.base;
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, base);
    }
}

class Manager extends Employee {
    private final int bonus;

    Manager(String name, int base, int bonus) {
        super(name, base);
        this.bonus = bonus;
    }

    @Override
    int pay() {
        return base() + bonus;
    }

    @Override
    Employee withRaise(int extra) {
        return new Manager(name(), base() + extra, bonus);
    }

    @Override
    public boolean equals(Object other) {
        return super.equals(other) && bonus == ((Manager) other).bonus;
    }

    @Override
    public int hashCode() {
        return Objects.hash(super.hashCode(), bonus);
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
