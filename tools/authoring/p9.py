import build, datetime, re
from zoneinfo import ZoneInfo
from collections import Counter

# ======================================================================== Stage 2 Category A
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-2"
from proj import *

def a1(amounts): return f"balance={sum(a for a in amounts)}"
def a2(overdraft, amounts):
    bal, refused = 0, 0
    for a in amounts:
        if a >= 0: bal += a
        elif bal + a < -overdraft: refused += 1
        else: bal += a
    return f"balance={bal} refused={refused}"
def a3(amounts):
    bal, n = 0, 0
    for a in amounts:
        if a > 0: bal += a; n += 1
    return f"history={n} afterTamper={n}"
GUIDED_DRV = '''
// ---------------------------------------------------------------------------------------------
// The checks call these. They show how your class will be used. Don't change them.
// ---------------------------------------------------------------------------------------------

String m1(int[] amounts) {
    Account account = new Account(0);
    for (int amount : amounts) {
        account.deposit(amount);
    }
    return "balance=" + account.balance();
}

String m2(int overdraft, int[] amounts) {
    Account account = new Account(overdraft);
    int refused = 0;
    for (int amount : amounts) {
        if (amount >= 0) {
            account.deposit(amount);
        } else if (!account.withdraw(-amount)) {
            refused++;
        }
    }
    return "balance=" + account.balance() + " refused=" + refused;
}

String m3(int[] amounts) {
    Account account = new Account(0);
    for (int amount : amounts) {
        if (amount > 0) {
            account.deposit(amount);
        }
    }
    int before = account.history().size();
    List<Transaction> copy = account.history();
    try {
        copy.clear();
    } catch (UnsupportedOperationException e) {
        // a read-only list is fine too
    }
    return "history=" + before + " afterTamper=" + account.history().size();
}

void main() {
    // Optional: try your class out here.
}
'''
A_SOL = '''
// Brightbank, now with a class. Money is whole pence in an int.

record Transaction(int amount) {}

class Account {
    private final int overdraftLimit;
    private int balance;
    private final List<Transaction> history = new ArrayList<>();

    Account(int overdraftLimit) {
        this.overdraftLimit = overdraftLimit;
    }

    void deposit(int amount) {
        balance += amount;
        history.add(new Transaction(amount));
    }

    boolean withdraw(int amount) {
        if (balance - amount < -overdraftLimit) {
            return false;
        }
        balance -= amount;
        history.add(new Transaction(-amount));
        return true;
    }

    int balance() {
        return balance;
    }

    List<Transaction> history() {
        return new ArrayList<>(history);
    }
}
''' + GUIDED_DRV
A_STARTER = '''// Brightbank, now with a class. Money is whole pence in an int.
// In Stage 1 an account was an int[] of transactions plus loose methods. Now the data and the rules live together.
// The class below compiles but its methods are stubs. Each milestone tells you what to write.

record Transaction(int amount) {}

class Account {
    // Step 1: what does an account remember? (fields)

    Account(int overdraftLimit) {
        // Step 2: store the overdraft limit
    }

    void deposit(int amount) {
    }

    boolean withdraw(int amount) {
        return false;
    }

    int balance() {
        return 0;
    }

    List<Transaction> history() {
        return List.of();
    }
}
''' + GUIDED_DRV
S = A_SOL
a_wrongs = {
  "m1-forgets-the-balance": S.replace("        balance += amount;\n        history.add(new Transaction(amount));", "        history.add(new Transaction(amount));"),
  "m2-overdraft-exclusive": S.replace("if (balance - amount < -overdraftLimit) {", "if (balance - amount <= -overdraftLimit) {"),
  "m3-leaks-the-history": S.replace("        return new ArrayList<>(history);", "        return history;"),
}
ams = [
 dict(id="m1", title="A class that remembers its balance", methods=[("m1", [("amounts", "int[]")], "String")], fns={"m1": a1},
  instructions="""
  In Stage 1 the account was an `int[]`; to find the balance you called a method and passed the array. A **class** keeps the data and the methods together.

  **Step 1.** Give `Account` a `private int balance` field (it starts at 0), and a `private final int overdraftLimit`.
  **Step 2.** Make the constructor store `overdraftLimit` (use `this.overdraftLimit = overdraftLimit;`).
  **Step 3.** `deposit(int amount)` adds the amount to `balance`. Don't forget it must also be recorded in the history (next milestone), but for now the balance matters.
  **Step 4.** `balance()` returns the balance.

  The check deposits a list of amounts and reads the balance.
  """,
  visible=[(None, [[100, 250]]), (None, [[]]), (None, [[5]])],
  hidden=[(None, [[1, 1, 1, 1]], "four ones"), (None, [[1000]], "one large deposit"), (None, [[0, 0]], "zero deposits"), (None, [[10, 20, 30, 40, 50]], "five deposits"), (None, [[-5, 10]], "a negative amount just adds")]),
 dict(id="m2", title="Withdrawals and the overdraft rule", methods=[("m2", [("overdraft", "int"), ("amounts", "int[]")], "String")], fns={"m2": a2},
  instructions="""
  A withdrawal is allowed only if the balance after it **doesn't fall below minus the overdraft limit**. With an overdraft of 100, a balance of -100 is fine; -101 is not.

  **Step 1.** `withdraw(int amount)` checks `balance - amount < -overdraftLimit`. If so, return `false` and **change nothing**.
  **Step 2.** Otherwise subtract the amount and return `true`.

  The check treats positive numbers as deposits and negative numbers as withdrawals of that size, and counts how many were refused.
  """,
  visible=[(None, [0, [100, -30, -200]]), (None, [50, [-50, -1]]), (None, [0, []])],
  hidden=[(None, [100, [-100]], "exactly to the limit"), (None, [100, [-101]], "one past the limit"), (None, [0, [100, -100, -1]], "exactly to zero then refused"), (None, [10, [5, -15, -1]], "uses the overdraft"), (None, [0, [-1, -1, -1]], "all refused")]),
 dict(id="m3", title="A history that can't be changed from outside", methods=[("m3", [("amounts", "int[]")], "String")], fns={"m3": a3},
  instructions="""
  Every successful deposit and withdrawal should be recorded as a `Transaction` (a record holding the amount; negative for a withdrawal).

  **Step 1.** Add a `private final List<Transaction> history = new ArrayList<>();` field, and `history.add(new Transaction(...))` in `deposit` and in a successful `withdraw`.
  **Step 2.** `history()` returns the list, **but a copy**: `return new ArrayList<>(history);`. If you return the field itself, code outside can call `clear()` on it and wipe your account's history. (This is the *defensive copy* idea from the lesson on immutability.)

  The check deposits some amounts, then tries to clear the list it was given, and looks at the history again.
  """,
  visible=[(None, [[100, 250]]), (None, [[]]), (None, [[5, 5, 5]])],
  hidden=[(None, [[1]], "one deposit"), (None, [[10, 20, 30, 40]], "four deposits"), (None, [[0]], "zero is not recorded by the check"), (None, [[7, 7]], "equal deposits"), (None, [[100, -5, 50]], "negative amounts are skipped by the driver")]),
]
project("j2-p0-brightbank-classes", "Brightbank as a class", "A",
    "A guided first refactor: turn Stage 1's array-and-methods account into an Account class, one small step at a time.",
    """
    In Stage 1 you wrote Brightbank as an `int[]` of transactions and loose methods. This guided project rebuilds the same ideas as a **class**, in three small milestones. Each milestone explains what to write and why; you fill in the code.

    The next project, **Brightbank as classes** (`j2-p1-brightbank`), is independent: it gives you only requirements. Do this one first if you want a gentler start.
    """, 2, ["j2-l1.2", "j2-l2.1", "j2-l2.2"], ["J2.01", "J2.02", "J2.05", "J2.06"],
    None, None, None, ams, None, None, A_STARTER, A_SOL, a_wrongs)

# ======================================================================== Stage 2 Category C
def staff_equal(name, base, bonus): return "false,false,true,false"
def unique_staff(names, bases, bonuses):
    return len({("E" if b < 0 else "M", n, base, 0 if b < 0 else b) for n, base, b in zip(names, bases, bonuses)})
def raise_(name, base, bonus, extra):
    before = base + (bonus if bonus >= 0 else 0)
    return f"{before}->{before + extra}"
SDRV = '''
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
'''
S_INHERITED = '''
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
'''
S_FINAL = '''
class Employee {
    private final String name;
    private final int base;

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
'''
SSOL = S_FINAL + SDRV
SSTART = S_INHERITED + SDRV
sw = {
  "m1-equals-still-instanceof": SSOL.replace("if (other == null || getClass() != other.getClass()) {", "if (!(other instanceof Employee)) {"),
  "m2-hash-uses-identity": SSOL.replace("        return Objects.hash(name, base);", "        return System.identityHashCode(this);").replace("        return Objects.hash(super.hashCode(), bonus);", "        return System.identityHashCode(this);"),
  "m3-raise-changes-the-original": S_INHERITED.replace('    @Override\n    public boolean equals(Object other) {\n        if (!(other instanceof Employee e)) {\n            return false;\n        }\n        return name.equals(e.name) && base == e.base;\n    }', '    @Override\n    public boolean equals(Object other) {\n        if (this == other) {\n            return true;\n        }\n        if (other == null || getClass() != other.getClass()) {\n            return false;\n        }\n        Employee e = (Employee) other;\n        return name.equals(e.name) && base == e.base;\n    }\n\n    @Override\n    public int hashCode() {\n        return Objects.hash(name, base);\n    }').replace('        if (!(other instanceof Manager m)) {\n            return false;\n        }\n        return super.equals(m) && bonus == m.bonus;', '        return super.equals(other) && bonus == ((Manager) other).bonus;') + SDRV,
  "m3-fields-not-private": SSOL.replace("    private final String name;\n    private final int base;", "    final String name;\n    final int base;"),
}
sms = [
 dict(id="m1", title="Equality that works both ways", methods=[("m1", [("name", "String"), ("base", "int"), ("bonus", "int")], "String")], fns={"m1": staff_equal},
  instructions="""
  **Ticket 311:** *"The staff list shows an employee and a manager as the same person in one direction only."*

  Reproduce it: for the same name and base pay, `employee.equals(manager)` and `manager.equals(employee)` give **different** answers. That breaks the rule that `equals` must be **symmetric**. Decide what the rule should be and fix it: **an `Employee` and a `Manager` are never equal**, even with the same name and base pay. Two managers are equal when name, base and bonus all match.

  The check prints four answers: `employee.equals(manager)`, `manager.equals(employee)`, `manager.equals(an identical manager)`, `manager.equals(a manager with a different bonus)`.
  """,
  visible=[(None, ["Ada", 3000, 500]), (None, ["Bo", 2000, 0]), (None, ["", 0, 1])],
  hidden=[(None, ["Cy", 100, 1], "small manager"), (None, ["Di", 5000, 9999], "large bonus"), (None, ["Ed", 1, 1], "tiny values")]),
 dict(id="m2", title="Sets of staff", methods=[("m2", [("names", "String[]"), ("bases", "int[]"), ("bonuses", "int[]")], "String")], fns={"m2": unique_staff},
  instructions="""
  **Ticket 312:** *"The same person appears several times in the staff set."*

  A `HashSet` finds duplicates with `hashCode` and then `equals`. These classes have `equals` but no `hashCode`, so equal staff land in different places. Add `hashCode` to both classes, **consistent with `equals`** (equal objects must have equal hash codes).

  The check adds employees (a negative bonus means a plain `Employee`) and managers to a set and counts how many distinct people it holds.
  """,
  visible=[(None, [["Ada", "Ada"], [3000, 3000], [-1, -1]]), (None, [["Ada", "Bo"], [3000, 3000], [-1, -1]]), (None, [[], [], []])],
  hidden=[(None, [["Ada", "Ada", "Ada"], [10, 10, 10], [5, 5, 5]], "three equal managers"), (None, [["Ada", "Ada"], [10, 10], [5, -1]], "a manager and an employee are different"), (None, [["Ada", "Ada"], [10, 10], [5, 6]], "different bonuses"), (None, [["X", "Y", "X", "Y"], [1, 2, 1, 2], [-1, -1, -1, -1]], "two pairs"), (None, [["Z"], [7], [0]], "bonus zero is still a manager")]),
 dict(id="m3", title="Respond to the review", methods=[("m3", [("name", "String"), ("base", "int"), ("bonus", "int"), ("extra", "int")], "String")], fns={"m3": raise_},
  instructions="""
  You open a pull request. The reviewer writes:

  > *"`withRaise` changes the employee it's called on and returns it. Two lists that share the same `Employee` will both see the raise. Staff should be **immutable**: make the fields `private final`, and have `withRaise` return a **new** object (a `Manager` for a manager) and leave the original alone."*

  Make the fields `private final` (add accessor methods if you need them) and fix `withRaise`. The check prints the pay of the original and of the raised copy, as `before->after`; the original's pay mustn't change.
  """,
  visible=[(None, ["Ada", 3000, -1, 200]), (None, ["Bo", 2000, 500, 100]), (None, ["Cy", 100, 0, 0])],
  hidden=[(None, ["Di", 1000, -1, 1], "plain employee, small raise"), (None, ["Ed", 1000, 250, 750], "manager keeps the bonus"), (None, ["Flo", 0, 0, 5], "from zero"), (None, ["Gus", 500, 100, -50], "a pay cut")],
  source_tests=[("the fields are private and final", ["private final String name", "private final int base"], None)]),
]
srub = [
 ("Reproduce, then fix", "Changed the code without showing the symptom first", "Showed one of the symptoms but fixed without saying why", "Reproduced each ticket with a specific case, and explained the broken rule (symmetry, the hashCode contract, aliasing)"),
 ("Design of equals and hashCode", "equals and hashCode disagree, or equals is still asymmetric", "Correct, but hashCode ignores part of what equals compares or uses a poor combination", "equals and hashCode use the same fields, are symmetric, and treat different classes as different"),
 ("Immutability", "Fields are still changeable, or the raise still changes the original", "Fields are final but a copy shares something changeable", "Private final fields; the raise returns a new object of the right class; the original is untouched"),
 ("Design note", "Missing, or just describes the code", "Describes the fixes but not the rules behind them", "Explains why equal objects need equal hash codes and why subclass equality is tricky, and what you'd change if another staff type arrived"),
]
project("j2-a1-inherited-staff", "The staff model nobody trusted", "C",
    "Take over a small class hierarchy with design weaknesses, fix two tickets, and respond to a review that asks for immutability.",
    """
    You've inherited the payroll system's staff classes: an `Employee` and a `Manager` that extends it. People have stopped trusting them. Three problems have been reported:

    1. **Ticket 311:** `equals` between an employee and a manager gives different answers depending on which one you call it on.
    2. **Ticket 312:** a `HashSet` of staff keeps duplicates.
    3. **Review:** the `withRaise` method changes the object it's called on, which surprises anyone sharing that object.

    This is a **diagnosis**, not a build: for each problem, reproduce it, find the broken rule, and fix it without breaking the others. Don't change the callers (`m1`, `m2`, `m3`). Your design note should say what rule each fix restores.
    """, 3, ["j2-l1.4", "j2-l2.2", "j2-l3.2"], ["J2.04", "J2.06", "J2.08"],
    ["`equals` is symmetric: an `Employee` and a `Manager` are never equal.",
     "Equal staff have equal hash codes, so a `HashSet` holds each person once.",
     "Staff are immutable: `withRaise` returns a new object and leaves the original alone."],
    ["Fix one ticket at a time and run all the checks after each.", "Don't change the callers."],
    ["Given an employee and a manager with the same name and base, then `equals` is false in both directions.",
     "Given the same manager added to a set three times, then the set holds one.",
     "Given a raise, then the original's pay is unchanged and the raised copy's pay is higher.",
     "Given the fixes, then all earlier checks still pass."],
    sms, srub,
    "In 150 words or fewer: For each ticket, say which rule was broken and how your fix restores it. Why is `equals` tricky when a subclass adds a field? What would you do if a third kind of staff, `Contractor`, were added?",
    SSTART, SSOL, sw)

# ======================================================================== Stage 3 Category C
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-3"
import importlib, proj
importlib.reload(proj)
from proj import project as project3
LONDON = ZoneInfo("Europe/London")
LEVELS = {"DEBUG", "INFO", "WARN", "ERROR"}
def parse(line):
    parts = line.split(" ", 2)
    if len(parts) < 3: return None
    ts, level = parts[0], parts[1]
    if level not in LEVELS: return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", ts): return None
    try: dt = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except ValueError: return None
    return dt, level
def per_day(lines):
    c = {}
    for ln in lines:
        p = parse(ln)
        if p and p[1] == "ERROR":
            d = p[0].astimezone(LONDON).date().isoformat(); c[d] = c.get(d, 0) + 1
    return ",".join(f"{k}={c[k]}" for k in sorted(c))
def bad_lines(lines): return sum(1 for ln in lines if parse(ln) is None)
def commonest(lines):
    c = Counter(p[1] for p in (parse(ln) for ln in lines) if p)
    return sorted(c, key=lambda k: (-c[k], k))[0] if c else ""
def gen_lines(n):
    levels = ["INFO", "WARN", "ERROR", "DEBUG"]
    out = []
    for i in range(n):
        out.append(f"2026-07-01T{(i * 7) % 24:02d}:{(i * 13) % 60:02d}:00Z {levels[(i * i + i // 3) % 4]} event {i}")
    return out
def m2(n): return commonest(gen_lines(n))
LDRV = '''
// ---------------------------------------------------------------------------------------------
// The callers. Don't change them.
// ---------------------------------------------------------------------------------------------

String m2(int n) {
    String[] levels = {"INFO", "WARN", "ERROR", "DEBUG"};
    List<String> lines = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        lines.add(String.format("2026-07-01T%02d:%02d:00Z %s event %d", (i * 7) % 24, (i * 13) % 60, levels[(int) (((long) i * i + i / 3) % 4)], i));
    }
    return commonestLevel(lines);
}

void main() {
    // Optional: try the analyser out here.
}
'''
L_INHERITED = '''
// INHERITED CODE: the log analyser. A line looks like:  2026-07-01T23:30:00Z ERROR disk full
// The time is always UTC (the Z). The operations team works in London time.

// Errors per day, as "2026-07-01=2,2026-07-02=1", sorted by day.
String errorsPerDay(List<String> lines) {
    Map<String, Integer> perDay = new TreeMap<>();
    for (String line : lines) {
        String[] parts = line.split(" ", 3);
        if (parts[1].equals("ERROR")) {
            String day = parts[0].substring(0, 10);
            perDay.merge(day, 1, Integer::sum);
        }
    }
    return perDay.entrySet().stream()
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining(","));
}

// The level that appears most often; on a tie, the alphabetically first.
String commonestLevel(List<String> lines) {
    List<String> levels = new ArrayList<>();
    for (String line : lines) {
        levels.add(line.split(" ", 3)[1]);
    }
    String best = "";
    int bestCount = 0;
    for (String level : levels) {
        int count = Collections.frequency(levels, level);
        if (count > bestCount || (count == bestCount && level.compareTo(best) < 0)) {
            best = level;
            bestCount = count;
        }
    }
    return best;
}

// How many lines are not well formed.
int badLines(List<String> lines) {
    return 0;
}
'''
L_FINAL = '''
// A line is well formed if it has a timestamp (UTC, ending in Z), a known level and a message.
// Returns null for a line that is not.
record Entry(Instant time, String level) {}

Entry parseLine(String line) {
    String[] parts = line.split(" ", 3);
    if (parts.length < 3) {
        return null;
    }
    if (!Set.of("DEBUG", "INFO", "WARN", "ERROR").contains(parts[1])) {
        return null;
    }
    try {
        return new Entry(Instant.parse(parts[0]), parts[1]);
    } catch (DateTimeParseException e) {
        return null;
    }
}

// Errors per day in London time, as "2026-07-01=2,2026-07-02=1", sorted by day.
String errorsPerDay(List<String> lines) {
    Map<String, Integer> perDay = new TreeMap<>();
    for (String line : lines) {
        Entry entry = parseLine(line);
        if (entry != null && entry.level().equals("ERROR")) {
            String day = entry.time().atZone(ZoneId.of("Europe/London")).toLocalDate().toString();
            perDay.merge(day, 1, Integer::sum);
        }
    }
    return perDay.entrySet().stream()
            .map(e -> e.getKey() + "=" + e.getValue())
            .collect(Collectors.joining(","));
}

// The level that appears most often; on a tie, the alphabetically first.
String commonestLevel(List<String> lines) {
    Map<String, Integer> counts = new TreeMap<>();
    for (String line : lines) {
        Entry entry = parseLine(line);
        if (entry != null) {
            counts.merge(entry.level(), 1, Integer::sum);
        }
    }
    String best = "";
    int bestCount = 0;
    for (Map.Entry<String, Integer> e : counts.entrySet()) {
        if (e.getValue() > bestCount) {
            best = e.getKey();
            bestCount = e.getValue();
        }
    }
    return best;
}

// How many lines are not well formed.
int badLines(List<String> lines) {
    int bad = 0;
    for (String line : lines) {
        if (parseLine(line) == null) {
            bad++;
        }
    }
    return bad;
}
'''
LSOL = L_FINAL + LDRV
LSTART = L_INHERITED + LDRV
W = ["2026-07-01T23:30:00Z ERROR disk full", "2026-07-01T10:00:00Z ERROR timeout", "2026-07-02T09:00:00Z ERROR timeout", "2026-07-02T10:00:00Z INFO started"]
lw = {
  "m1-always-plus-one-hour": LSOL.replace("entry.time().atZone(ZoneId.of(\"Europe/London\"))", "entry.time().plusSeconds(3600).atZone(ZoneId.of(\"UTC\"))"),
  "m2-ties-go-last": LSOL.replace("if (e.getValue() > bestCount) {", "if (e.getValue() >= bestCount) {"),
  "m3-crashes-on-bad-lines": L_INHERITED.replace('String day = parts[0].substring(0, 10);', 'String day = Instant.parse(parts[0]).atZone(ZoneId.of("Europe/London")).toLocalDate().toString();') + LDRV,
  "m3-counts-unknown-levels-as-good": LSOL.replace('    if (!Set.of("DEBUG", "INFO", "WARN", "ERROR").contains(parts[1])) {\n        return null;\n    }\n', ''),
}
lms = [
 dict(id="m1", title="Errors on the wrong day", methods=[("errorsPerDay", [("lines", "List<String>")], "String")], fns={"errorsPerDay": per_day},
  instructions="""
  **Ticket 77:** *"The daily error report is wrong for errors just before midnight UTC. The team works in London time."*

  `errorsPerDay` groups `ERROR` lines by the date in the **timestamp text**, which is UTC. In summer, London is an hour ahead of UTC, so `2026-07-01T23:30:00Z` is already **2 July** in London. In winter London is the same as UTC. Reproduce it with that line, find the cause, and fix it using `java.time` and the zone `Europe/London`. Don't add a fixed hour: the offset changes with the clocks.

  For now, every line in the checks is well formed.
  """,
  visible=[(None, [W]), (None, [[]]), (None, [["2026-01-15T23:30:00Z ERROR winter"]])],
  hidden=[(None, [["2026-06-30T23:30:00Z ERROR a", "2026-07-01T00:00:00Z ERROR b"]], "summer, either side of midnight UTC"), (None, [["2026-03-29T00:30:00Z ERROR before the clocks change", "2026-03-29T01:30:00Z ERROR after"]], "the day the clocks go forward"), (None, [["2026-10-25T00:30:00Z ERROR a", "2026-10-25T23:30:00Z ERROR b"]], "the day the clocks go back"), (None, [["2026-12-31T23:59:59Z ERROR new year"]], "new year in winter"), (None, [["2026-07-01T10:00:00Z INFO only info"]], "no errors")]),
 dict(id="m2", title="The analyser that takes minutes", methods=[("m2", [("n", "int")], "String")], fns={"m2": m2},
  instructions="""
  **Ticket 78:** *"Finding the most common level takes minutes for a day's logs (300,000 lines). It must finish in under 2 seconds."*

  `commonestLevel` returns the most frequent level (the alphabetically first on a tie). It's correct. Measure it: what does `Collections.frequency` do, and how many times is it called? Fix the cost without changing any answer.
  """,
  visible=[(None, [10]), (None, [1]), (None, [0])],
  hidden=[(None, [300000], "a day of logs"), (None, [200000], "two hundred thousand lines"), (None, [3], "three lines")]),
 dict(id="m3", title="Respond to the review: bad lines", methods=[("errorsPerDay", [("lines", "List<String>")], "String"), ("badLines", [("lines", "List<String>")], "int")], fns={"errorsPerDay": per_day, "badLines": bad_lines},
  instructions="""
  In review, the operations lead says: *"Last week a truncated line crashed the whole report. A malformed line must be **skipped and counted**, never crash it."*

  A line is **well formed** if it has at least three parts separated by spaces: a timestamp that `Instant.parse` accepts, a level that is one of `DEBUG`, `INFO`, `WARN`, `ERROR`, and then the message. Make `errorsPerDay` (and `commonestLevel`) ignore malformed lines, and implement `badLines`, which counts them. Well-formed lines must behave exactly as before.
  """,
  visible=[("errorsPerDay", [W + ["garbage"]]), ("badLines", [["garbage", "2026-07-01T10:00:00Z INFO ok"]]), ("badLines", [[]])],
  hidden=[("errorsPerDay", [["", "2026-07-01T10:00:00Z", "not-a-time ERROR x", "2026-07-01T10:00:00Z ERROR ok"]], "several kinds of bad line"), ("badLines", [["2026-07-01T10:00:00Z LOUD message"]], "unknown level"), ("badLines", [["2026-07-01T10:00:00Z ERROR a", "2026-07-01T10:00:00Z WARN b"]], "none bad"), ("badLines", [["2026-13-01T10:00:00Z ERROR impossible month"]], "impossible date"), ("errorsPerDay", [["2026-07-01T23:30:00Z ERROR late", "broken line"]], "a good line next to a bad one")]),
]
lrub = [
 ("Diagnosis", "Changed code without finding the cause", "Fixed the bugs but can't explain why they happened", "Names the cause of each problem: grouping by UTC text, a hidden quadratic scan, and parsing without validation"),
 ("Time handling", "Added a fixed offset, or still groups by the text", "Uses `java.time` but with the wrong zone or for only part of the year", "Converts each instant to `Europe/London` with `java.time`, correct on both sides of both clock changes"),
 ("Evidence and requirement", "No measurement against the two-second requirement", "Measured only the final result", "Measured or counted steps before and after, and met the requirement on the large input"),
 ("Design note", "Missing, or just says what changed", "Says what changed but not why", "Explains each growth rate, why a fixed hour would be wrong, and how bad lines are reported"),
]
project3("j3-a1-log-analyser", "The log analyser that gets the day wrong", "C",
    "Inherit a log analyser with a time-zone bug and a performance bug, fix both against measured requirements, and respond to a review about bad lines.",
    """
    You've inherited a small log analyser. Operations use it every morning. It has three problems, each reported as a ticket or a review comment:

    1. **The day is wrong** for errors near midnight, because the report groups by the UTC date in the text, but the team works in London time.
    2. **It's far too slow** on a day's logs.
    3. **One bad line crashes it.**

    This is a **diagnosis**: reproduce each problem, find the cause, fix it, and keep every other answer the same. Use `java.time` for the time zone (not a fixed number of hours: the offset changes twice a year). Don't change the callers. A design note at the end says what you found.
    """, 4, ["j3-l4.2", "j3-l5.1", "j3-l3.2"], ["J3.06", "J3.09", "J3.10"],
    ["`errorsPerDay` groups `ERROR` lines by their **London** date, correctly in both summer and winter.",
     "`commonestLevel` finishes in under 2 seconds on 300,000 lines, with the same answers.",
     "A malformed line is skipped and counted (`badLines`), and never crashes a report.",
     "Well-formed lines behave exactly as before."],
    ["Use `java.time` and the zone `Europe/London`; no fixed hour offsets.", "Don't change the callers."],
    ["Given `2026-07-01T23:30:00Z ERROR x`, then it counts on 2 July.",
     "Given `2026-01-15T23:30:00Z ERROR x`, then it counts on 15 January.",
     "Given 300,000 lines, then the commonest level is found in time.",
     "Given a truncated line, then the report still runs and `badLines` counts it."],
    lms, lrub,
    "In 150 words or fewer: What was wrong with grouping by the text, and why would adding one hour be wrong too? What made the analyser slow, and what is its growth rate before and after? How are malformed lines handled, and where would you report them?",
    LSTART, LSOL, lw)
print("P9 written")
