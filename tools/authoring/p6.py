import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-3"
from proj import *
import re, datetime
from decimal import Decimal

def fmt(p):
    sign = "-" if p < 0 else ""
    a = abs(p)
    return f"{sign}£{a // 100}.{a % 100:02d}"

def parse_line(raw):
    parts = raw.split(",")
    if len(parts) != 3: return None
    d, desc, amt = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if desc == "" or not re.fullmatch(r"[+-]?[0-9]+(\.[0-9]{1,2})?", amt): return None
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", d): return None
    try: date = datetime.date.fromisoformat(d)
    except ValueError: return None
    return (date, desc, int(Decimal(amt) * 100))

def parse_all(lines):
    good, bad, seen, dupes = [], 0, set(), 0
    for raw in lines:
        line = raw.strip()
        if line == "" or line.lower() == "date,description,amount": continue
        t = parse_line(raw)
        if t is None: bad += 1; continue
        if t in seen: dupes += 1; continue
        seen.add(t); good.append(t)
    return good, bad, dupes

def summary(lines):
    good, bad, _ = parse_all(lines)
    return f"ok={len(good)} bad={bad}"
def monthly(lines):
    good, _, _ = parse_all(lines)
    tot = {}
    for d, _, p in good:
        k = f"{d.year}-{d.month:02d}"
        tot[k] = tot.get(k, 0) + p
    return ",".join(f"{k}={tot[k]:+d}" for k in sorted(tot)) or "none"
def statement(lines, a, b):
    good, _, _ = parse_all(lines)
    fa, fb = datetime.date.fromisoformat(a), datetime.date.fromisoformat(b)
    inside = [t for t in good if fa <= t[0] <= fb]
    inside = sorted(inside, key=lambda t: t[0], reverse=True)
    rows = [f"{t[0].isoformat()} {t[1]} {fmt(t[2])}" for t in inside]
    return "\n".join(rows + [f"Total: {fmt(sum(t[2] for t in inside))}"])
def unique_summary(lines):
    good, bad, dupes = parse_all(lines)
    return f"ok={len(good)} bad={bad} dupes={dupes}"

PRELUDE = '''
class Money {
    static String format(int pence) {
        String sign = pence < 0 ? "-" : "";
        int absolute = Math.abs(pence);
        String padding = absolute % 100 < 10 ? "0" : "";
        return sign + "£" + absolute / 100 + "." + padding + absolute % 100;
    }
}
'''
SOLUTION = PRELUDE + '''
record Transaction(LocalDate date, String description, int pence) {}

record Parsed(List<Transaction> good, int bad, int duplicates) {}

// One line is "date,description,amount". Returns null for a line that isn't valid.
Transaction parseLine(String raw) {
    String[] parts = raw.split(",", -1);
    if (parts.length != 3) {
        return null;
    }
    String description = parts[1].strip();
    String amountText = parts[2].strip();
    if (description.isEmpty() || !amountText.matches("[+-]?[0-9]+(\\\\.[0-9]{1,2})?")) {
        return null;
    }
    LocalDate date;
    try {
        date = LocalDate.parse(parts[0].strip());
    } catch (DateTimeParseException e) {
        return null;
    }
    int pence = new BigDecimal(amountText).movePointRight(2).intValueExact();
    return new Transaction(date, description, pence);
}

Parsed parseAll(List<String> lines) {
    Set<Transaction> unique = new LinkedHashSet<>();
    int bad = 0;
    int duplicates = 0;
    for (String raw : lines) {
        String line = raw.strip();
        if (line.isEmpty() || line.equalsIgnoreCase("date,description,amount")) {
            continue;
        }
        Transaction t = parseLine(raw);
        if (t == null) {
            bad++;
        } else if (!unique.add(t)) {
            duplicates++;
        }
    }
    return new Parsed(new ArrayList<>(unique), bad, duplicates);
}

String summary(List<String> lines) {
    Parsed p = parseAll(lines);
    return "ok=" + p.good().size() + " bad=" + p.bad();
}

String monthlyTotals(List<String> lines) {
    Map<String, Integer> totals = new TreeMap<>();
    for (Transaction t : parseAll(lines).good()) {
        String month = String.format("%d-%02d", t.date().getYear(), t.date().getMonthValue());
        totals.merge(month, t.pence(), Integer::sum);
    }
    if (totals.isEmpty()) {
        return "none";
    }
    return totals.entrySet().stream()
            .map(e -> e.getKey() + "=" + String.format("%+d", e.getValue()))
            .collect(Collectors.joining(","));
}

String statement(List<String> lines, String from, String to) {
    LocalDate start = LocalDate.parse(from);
    LocalDate end = LocalDate.parse(to);
    List<Transaction> inside = new ArrayList<>(parseAll(lines).good().stream()
            .filter(t -> !t.date().isBefore(start) && !t.date().isAfter(end))
            .toList());
    inside.sort(Comparator.comparing(Transaction::date).reversed());
    StringBuilder text = new StringBuilder();
    int total = 0;
    for (Transaction t : inside) {
        text.append(t.date()).append(" ").append(t.description()).append(" ").append(Money.format(t.pence())).append("\\n");
        total += t.pence();
    }
    return text + "Total: " + Money.format(total);
}

String uniqueSummary(List<String> lines) {
    Parsed p = parseAll(lines);
    return "ok=" + p.good().size() + " bad=" + p.bad() + " dupes=" + p.duplicates();
}

void main() {
    // Optional: try your methods out here.
}
'''
STARTER = '''// Brightbank v3: read a bank's CSV export. Each line is  date,description,amount  (amount in pounds, e.g. -2.50).
// Money.format is given. The methods below compile but return wrong answers. The brief says what each must do.
''' + PRELUDE + '''
String summary(List<String> lines) {
    return "";
}

String monthlyTotals(List<String> lines) {
    return "";
}

String statement(List<String> lines, String from, String to) {
    return "";
}

String uniqueSummary(List<String> lines) {
    return "";
}

void main() {
    // Optional: try your methods out here.
}
'''
S = SOLUTION
wrongs = {
  "m1-blank-lines-are-bad": S.replace("if (line.isEmpty() || line.equalsIgnoreCase(\"date,description,amount\")) {\n            continue;\n        }", "if (line.equalsIgnoreCase(\"date,description,amount\")) {\n            continue;\n        }"),
  "m1-three-decimals-allowed": S.replace("{1,2}", "{1,3}"),
  "m1-invalid-dates-allowed": S.replace("date = LocalDate.parse(parts[0].strip());", "date = LocalDate.of(Integer.parseInt(parts[0].strip().substring(0, 4)), Integer.parseInt(parts[0].strip().substring(5, 7)), Math.min(Integer.parseInt(parts[0].strip().substring(8, 10)), 28));"),
  "m2-insertion-order": S.replace("new TreeMap<>()", "new LinkedHashMap<>()"),
  "m2-absolute-amounts": S.replace("totals.merge(month, t.pence(), Integer::sum);", "totals.merge(month, Math.abs(t.pence()), Integer::sum);"),
  "m3-oldest-first": S.replace("Comparator.comparing(Transaction::date).reversed()", "Comparator.comparing(Transaction::date)"),
  "m3-excludes-last-day": S.replace("!t.date().isAfter(end)", "t.date().isBefore(end)"),
  "m4-duplicates-counted": S.replace("} else if (!unique.add(t)) {\n            duplicates++;\n        }", "} else {\n            unique.add(t);\n            list.add(t);\n        }").replace("Set<Transaction> unique = new LinkedHashSet<>();", "Set<Transaction> unique = new LinkedHashSet<>();\n    List<Transaction> list = new ArrayList<>();").replace("return new Parsed(new ArrayList<>(unique), bad, duplicates);", "return new Parsed(list, bad, duplicates);"),
  "m4-duplicates-by-date-only": S.replace("} else if (!unique.add(t)) {\n            duplicates++;\n        }", "} else if (!seenDates.add(t.date())) {\n            duplicates++;\n        } else {\n            unique.add(t);\n        }").replace("Set<Transaction> unique = new LinkedHashSet<>();", "Set<Transaction> unique = new LinkedHashSet<>();\n    Set<LocalDate> seenDates = new HashSet<>();"),
}
G = ["date,description,amount", "2026-01-05,Coffee,-2.50", "2026-01-06,Salary,1200", "2026-02-01,Rent,-500.00"]
ms = [
 dict(id="m1", title="Read the file, keep the good lines", methods=[("summary", [("lines", "List<String>")], "String")], fns={"summary": summary},
  instructions="""
  Each line of the export is `date,description,amount`. Write `summary(lines)`, which returns `ok=<n> bad=<m>`: how many lines are good, and how many are bad.

  - **Skip** blank lines and the header line `date,description,amount` (any case). Skipped lines are neither good nor bad.
  - A line is **bad** if it doesn't have exactly three fields, the description is empty, the date isn't a real date in `yyyy-MM-dd` form (`2026-02-30` is not real), or the amount isn't a number with at most **two** digits after the point (an optional `+` or `-` sign is allowed). Ignore spaces around each field.
  - Keep money exact: don't use `double`.
  """,
  visible=[(None, [G]), (None, [[]]), (None, [["2026-01-05,Coffee,-2.50", "oops"]])],
  hidden=[(None, [["2026-02-30,Impossible,1.00"]], "not a real date"), (None, [["2026-01-05,Coffee,2.505"]], "three decimals"), (None, [["2026-01-05,,5.00"]], "empty description"), (None, [["2026-01-05,Tea,+5.5", " 2026-01-06 , Cake , -0.99 "]], "sign and spaces"), (None, [["", "   ", "DATE,DESCRIPTION,AMOUNT"]], "only skipped lines"), (None, [["2026-1-5,Tea,5.00", "2026-01-05,Tea,5.00,extra"]], "bad shapes")]),
 dict(id="m2", title="Totals by month", methods=[("monthlyTotals", [("lines", "List<String>")], "String")], fns={"monthlyTotals": monthly},
  instructions="""
  Write `monthlyTotals(lines)`: the **net total in pence** for each month that has good transactions, **sorted by month**, as `2026-01=+1197,2026-02=-50000`, joined with commas. The sign is always shown. If there are no good transactions, return `none`.
  """,
  visible=[(None, [G]), (None, [[]]), (None, [["2026-03-01,A,10.00", "2026-03-02,B,-3.50"]])],
  hidden=[(None, [["2026-12-31,Late,1.00", "2026-01-01,Early,2.00"]], "months out of order"), (None, [["2026-05-05,A,5.00", "2026-05-06,B,-5.00"]], "nets to zero"), (None, [["bad", "2026-04-04,Ok,0.99"]], "bad lines ignored"), (None, [["2025-12-31,A,100", "2026-01-01,B,100", "2026-01-31,C,-0.01"]], "year boundary")]),
 dict(id="m3", title="A statement for a date range", methods=[("statement", [("lines", "List<String>"), ("from", "String"), ("to", "String")], "String")], fns={"statement": statement},
  instructions="""
  Write `statement(lines, from, to)` (both dates `yyyy-MM-dd`). It returns text lines separated by `\\n` (none after the last):

  - the good transactions dated from `from` to `to`, **both days included**, **newest first**, each as `2026-01-06 Salary £1200.00` (a negative amount shows as `-£2.50`); transactions on the same day keep the order they had in the file;
  - then a last line `Total: ` with the net total of the listed transactions.

  If none are in the range, there is only the total line (`Total: £0.00`).
  """,
  visible=[(None, [G, "2026-01-01", "2026-01-31"]), (None, [G, "2027-01-01", "2027-01-31"]), (None, [G, "2026-01-06", "2026-02-01"])],
  hidden=[(None, [G, "2026-01-05", "2026-01-05"], "a single day"), (None, [["2026-01-05,A,1.00", "2026-01-05,B,2.00", "2026-01-04,C,3.00"], "2026-01-01", "2026-01-31"], "ties keep file order"), (None, [G, "2026-01-06", "2026-01-05"], "range backwards"), (None, [["bad", "2026-01-05,Tea,-0.05"], "2026-01-01", "2026-12-31"], "pence padding")]),
 dict(id="m4", title="Change request: duplicate lines", methods=[("uniqueSummary", [("lines", "List<String>")], "String"), ("monthlyTotals", [("lines", "List<String>")], "String"), ("statement", [("lines", "List<String>"), ("from", "String"), ("to", "String")], "String")],
  fns={"uniqueSummary": unique_summary, "monthlyTotals": monthly, "statement": statement},
  instructions="""
  **A change request has arrived.** The bank's export sometimes repeats lines. A transaction repeated **exactly** (same date, description and amount) must count **once**, everywhere. Without breaking milestones 1 to 3:

  - add `uniqueSummary(lines)`, which returns `ok=<n> bad=<m> dupes=<k>`: `ok` counts each distinct good transaction once, `bad` is as before, and `dupes` is how many extra repeated copies were ignored;
  - make `monthlyTotals` and `statement` use each distinct transaction once, keeping the **first** copy's position.

  Two transactions that differ in the date, the description or the amount are **different**, even if the other two parts match. Decide where in your code one change fixes all three methods.
  """,
  visible=[("uniqueSummary", [G + [G[1]]]), ("monthlyTotals", [["2026-01-05,A,5.00", "2026-01-05,A,5.00"]]), ("statement", [["2026-01-05,A,5.00", "2026-01-05,A,5.00"], "2026-01-01", "2026-01-31"])],
  hidden=[("uniqueSummary", [["2026-01-05,A,5.00", "2026-01-05,A,5.00", "2026-01-05,A,5.00"]], "three copies"), ("uniqueSummary", [["2026-01-05,A,5.00", "2026-01-06,A,5.00", "2026-01-05,B,5.00", "2026-01-05,A,5.01"]], "all different"), ("uniqueSummary", [["bad", "bad"]], "bad lines repeat but aren't dupes"), ("monthlyTotals", [["2026-02-02,A,1.00", "2026-02-03,A,1.00", "2026-02-02,A,1.00"]], "different days stay"), ("statement", [["2026-01-05,A,1.00", "2026-01-06,B,2.00", "2026-01-05,A,1.00"], "2026-01-01", "2026-01-31"], "duplicate is removed from the statement")]),
]
rubric = [
 ("Correctness at the edges", "Several milestones fail on boundaries (a single day, pence padding, an impossible date, three decimals)", "Typical cases pass and most boundaries", "Every boundary in the brief behaves as specified, including the change request"),
 ("Use of the library", "Hand-written date or money arithmetic, or `double` for money", "Mostly `java.time` and exact money, with one hand-rolled part", "`java.time` for dates, exact money, and the right collection for each job (a sorted map, a set for duplicates)"),
 ("Handling the change request", "Milestones 1 to 3 broke, or the duplicate check was added in three places", "It works, but the fix was copied into more than one method", "One shared parsing step removes duplicates, so every method benefits and milestones 1 to 3 still pass"),
 ("Design note", "Missing, or describes the code line by line", "Explains the steps but not the choices", "Explains why money isn't a double, how bad lines are handled, and where the duplicate rule lives"),
]
project("j3-p1-brightbank", "Brightbank statements from a CSV", "B",
    "Read a bank's messy CSV export, total it by month, produce a statement for a date range, and absorb a change request about duplicates.",
    """
    Brightbank v3 reads the file a bank exports: a CSV of `date,description,amount` lines. Real exports are messy: a header, blank lines, impossible dates, odd amounts, and (as you'll find out) repeated lines.

    You'll use what Stage 3 taught: `java.time` for the dates, exact money (never `double`), a sorted map for the monthly totals, a stream or a loop for the statement, and a set to deal with duplicates.

    This is an **independent build** with a twist: partway through, a **change request** arrives (milestone 4). Where you put your parsing decides whether it's a one-line change or a three-place change.

    To keep the project to one file, the lines come in as a `List<String>`. In a real program you'd read them with `Files.readAllLines`, as in lesson 3.4.1.
    """, 6, ["j3-l1.2", "j3-l3.2", "j3-l4.2", "j3-l5.1", "j3-l5.2"], ["J3.02", "J3.03", "J3.06", "J3.09", "J3.10", "J3.11"],
    ["Each good line is `date,description,amount`, with the date in `yyyy-MM-dd` form and the amount in pounds with at most two decimals.",
     "A bad line is counted and skipped; it never stops the run.",
     "Money is exact: no `double`.",
     "Output formats are exactly as the milestones describe."],
    ["Parse each line once, in one place.", "Use `java.time` for dates; no hand-written calendar arithmetic."],
    ["Given `2026-02-30,X,1.00`, then it counts as a bad line.",
     "Given a statement for 2026-01-05 to 2026-01-05, then transactions on that day are included.",
     "Given the same transaction twice in the file, then it counts once in every output.",
     "Given the change request, then milestones 1 to 3 still pass unchanged."],
    ms, rubric,
    "In 150 words or fewer: How did you keep money exact, and what would have gone wrong with `double`? Where does your code decide that a line is a duplicate, and what would you change if the bank said duplicates should be judged by date and amount only?",
    STARTER, SOLUTION, wrongs)
print("P6 written")
