import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-5"
from proj import *
from collections import Counter

CA = '''
// Counts how many times get() is called, so the checks can tell a fast search from a slow one.
class CountingArray {
    private final int[] data;
    int reads;

    CountingArray(int[] data) {
        this.data = data;
    }

    int size() {
        return data.length;
    }

    int get(int index) {
        reads++;
        return data[index];
    }
}
'''

# ----- independent reference model -------------------------------------------------------------
def count_in_range(n, low, high):
    if low > high: return 0
    vals = [2 * i for i in range(n)] if n <= 2000 else None
    if vals is not None:
        return sum(1 for v in vals if low <= v <= high)
    lo_i = max(0, -((-low) // 2)); hi_i = min(n - 1, high // 2) if high >= 0 else -1
    return max(0, hi_i - lo_i + 1)
for n in (0, 1, 5, 50):
    for lo in range(-3, 2 * n + 3):
        for hi in range(lo - 1, 2 * n + 3, 3):
            vals = [2 * i for i in range(n)]
            exp = sum(1 for v in vals if lo <= v <= hi) if lo <= hi else 0
            lo_i = max(0, -((-lo) // 2)); hi_i = min(n - 1, hi // 2) if hi >= 0 else -1
            fast = 0 if lo > hi else max(0, hi_i - lo_i + 1)
            assert exp == fast, (n, lo, hi, exp, fast)
def m1(n, low, high): return f"{count_in_range(n, low, high)} fast=true"
def dups(ids):
    seen, rep = set(), []
    for i in ids:
        k = i.lower()
        if k in seen:
            if k not in rep: rep.append(k)
        else: seen.add(k)
    return rep
def m2(n):
    r = min(500, n // 2)
    ids = [f"t{i if i < n - r else i - (n - r)}" for i in range(n)]
    d = dups(ids)
    return f"size={len(d)} first={d[0] if d else '-'} last={d[-1] if d else '-'}"
def top(names, pence, n):
    tot = {}
    for nm, p in zip(names, pence): tot[nm.lower()] = tot.get(nm.lower(), 0) + p
    return [k for k, _ in sorted(tot.items(), key=lambda kv: (-kv[1], kv[0]))[:n]]
def m3(customers, n):
    names = [f"c{i % customers}" for i in range(customers * 3)]
    pence = [(i * 37) % 1000 + 1 for i in range(customers * 3)]
    return ",".join(top(names, pence, n))

SOLUTION_METHODS = '''
int countInRange(CountingArray amounts, int low, int high) {
    if (low > high) {
        return 0;
    }
    return upperBound(amounts, high) - lowerBound(amounts, low);
}

// First index whose value is at least target.
int lowerBound(CountingArray a, int target) {
    int lo = 0;
    int hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a.get(mid) < target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

// First index whose value is greater than target.
int upperBound(CountingArray a, int target) {
    int lo = 0;
    int hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a.get(mid) <= target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

List<String> duplicates(List<String> ids) {
    Set<String> seen = new HashSet<>();
    Set<String> reported = new LinkedHashSet<>();
    for (String id : ids) {
        String key = id.toLowerCase();
        if (!seen.add(key)) {
            reported.add(key);
        }
    }
    return new ArrayList<>(reported);
}

List<String> topSpenders(String[] names, int[] pence, int n) {
    Map<String, Long> totals = new HashMap<>();
    for (int i = 0; i < names.length; i++) {
        totals.merge(names[i].toLowerCase(), (long) pence[i], Long::sum);
    }
    List<Map.Entry<String, Long>> entries = new ArrayList<>(totals.entrySet());
    entries.sort((x, y) -> {
        int byTotal = Long.compare(y.getValue(), x.getValue());
        return byTotal != 0 ? byTotal : x.getKey().compareTo(y.getKey());
    });
    List<String> result = new ArrayList<>();
    for (int i = 0; i < Math.min(n, entries.size()); i++) {
        result.add(entries.get(i).getKey());
    }
    return result;
}
'''
DRIVERS = '''
// ---------------------------------------------------------------------------------------------
// The checks call these. They build large inputs for you. Don't change them.
// ---------------------------------------------------------------------------------------------

String m1(int n, int low, int high) {
    int[] data = new int[n];
    for (int i = 0; i < n; i++) {
        data[i] = i * 2;
    }
    CountingArray amounts = new CountingArray(data);
    int count = countInRange(amounts, low, high);
    int limit = 4 * (32 - Integer.numberOfLeadingZeros(Math.max(n, 1))) + 8;
    return count + " fast=" + (amounts.reads <= limit);
}

String m2(int n) {
    int r = Math.min(500, n / 2);
    List<String> ids = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        ids.add("t" + (i < n - r ? i : i - (n - r)));
    }
    List<String> d = duplicates(ids);
    return "size=" + d.size() + " first=" + (d.isEmpty() ? "-" : d.get(0)) + " last=" + (d.isEmpty() ? "-" : d.get(d.size() - 1));
}

String m3(int customers, int n) {
    int count = customers * 3;
    String[] names = new String[count];
    int[] pence = new int[count];
    for (int i = 0; i < count; i++) {
        names[i] = "c" + (i % customers);
        pence[i] = (i * 37) % 1000 + 1;
    }
    return String.join(",", topSpenders(names, pence, n));
}

void main() {
    // Optional: try your methods out here.
}
'''
SOLUTION = CA + SOLUTION_METHODS + DRIVERS
STARTER = '''// Brightbank v5: searching and summarising a very large statement.
// The checks count array reads and enforce a time limit, so the way you search and count matters.
// The methods below compile but return wrong answers. The brief says what each must do.
''' + CA + '''
int countInRange(CountingArray amounts, int low, int high) {
    return 0;
}

List<String> duplicates(List<String> ids) {
    return new ArrayList<>();
}

List<String> topSpenders(String[] names, int[] pence, int n) {
    return new ArrayList<>();
}
''' + DRIVERS
S = SOLUTION
wrongs = {
  "m1-linear-scan": S.replace("    return upperBound(amounts, high) - lowerBound(amounts, low);", "    int count = 0;\n    for (int i = 0; i < amounts.size(); i++) {\n        int v = amounts.get(i);\n        if (v >= low && v <= high) {\n            count++;\n        }\n    }\n    return count;"),
  "m1-excludes-the-top-end": S.replace("a.get(mid) <= target", "a.get(mid) < target"),
  "m2-quadratic": S.replace("    Set<String> seen = new HashSet<>();\n    Set<String> reported = new LinkedHashSet<>();\n    for (String id : ids) {\n        String key = id.toLowerCase();\n        if (!seen.add(key)) {\n            reported.add(key);\n        }\n    }\n    return new ArrayList<>(reported);", "    List<String> seen = new ArrayList<>();\n    List<String> reported = new ArrayList<>();\n    for (String id : ids) {\n        String key = id.toLowerCase();\n        if (seen.contains(key)) {\n            if (!reported.contains(key)) {\n                reported.add(key);\n            }\n        } else {\n            seen.add(key);\n        }\n    }\n    return reported;"),
  "m2-reports-every-repeat": S.replace("        if (!seen.add(key)) {\n            reported.add(key);\n        }", "        if (!seen.add(key)) {\n            reported.add(key + \"\");\n            if (reported.size() > 1000000) break;\n        }").replace("Set<String> reported = new LinkedHashSet<>();", "List<String> reported = new ArrayList<>();"),
  "m3-ties-unordered": S.replace("        return byTotal != 0 ? byTotal : x.getKey().compareTo(y.getKey());", "        return byTotal != 0 ? byTotal : y.getKey().compareTo(x.getKey());"),
  "m3-ascending": S.replace("Long.compare(y.getValue(), x.getValue())", "Long.compare(x.getValue(), y.getValue())"),
  "m4-still-case-sensitive": S.replace("String key = id.toLowerCase();", "String key = id;").replace("totals.merge(names[i].toLowerCase(),", "totals.merge(names[i],"),
}
ms = [
 dict(id="m1", title="Count a range in a sorted statement", methods=[("m1", [("n", "int"), ("low", "int"), ("high", "int")], "String")], fns={"m1": m1},
  instructions="""
  A statement's amounts are kept **sorted**. Write `countInRange(amounts, low, high)`, which counts how many amounts `x` satisfy `low <= x <= high`. The amounts are wrapped in a `CountingArray` (it counts every `get`), and the check also requires `fast=true`: you may read only about `4 * log2(n)` elements. So use **binary search**, twice: find the first index with a value at least `low`, and the first index with a value greater than `high`. The answer is the difference. If `low > high` the count is 0.

  The driver `m1` builds the amounts `0, 2, 4, ...` for you.
  """,
  visible=[(None, [10, 3, 9]), (None, [10, 0, 18]), (None, [10, 100, 200])],
  hidden=[(None, [1000000, 500, 1500], "a million amounts"), (None, [5000000, 1, 9999998], "five million amounts, nearly all"), (None, [10, 4, 4], "a single value"), (None, [10, 5, 5], "an absent value"), (None, [10, 9, 3], "low above high"), (None, [1, 0, 0], "one amount"), (None, [100, -50, 10], "range starting below the data")]),
 dict(id="m2", title="Duplicate transaction ids", methods=[("duplicates", [("ids", "List<String>")], "List<String>"), ("m2", [("n", "int")], "String")], fns={"duplicates": dups, "m2": m2},
  instructions="""
  Write `duplicates(ids)`: the ids that appear **more than once**, each reported **once**, in the order in which each id is first seen **a second time**. For `[a, b, a, c, b, a]` that is `[a, b]`.

  It has to be fast: the driver `m2` calls it with 200,000 ids under a 2-second limit. Think about which structure answers "have I seen this before?" in constant time.
  """,
  visible=[("duplicates", [["a", "b", "a", "c", "b", "a"]]), ("duplicates", [[]]), ("duplicates", [["x", "y", "z"]])],
  hidden=[("duplicates", [["q", "q", "q"]], "one id three times"), ("duplicates", [["a", "b", "b", "a"]], "order of second appearance"), ("m2", [200000], "two hundred thousand ids"), ("m2", [1000], "a thousand ids"), ("m2", [10], "ten ids"), ("m2", [0], "no ids")]),
 dict(id="m3", title="The top spenders", methods=[("topSpenders", [("names", "String[]"), ("pence", "int[]"), ("n", "int")], "List<String>"), ("m3", [("customers", "int"), ("n", "int")], "String")], fns={"topSpenders": top, "m3": m3},
  instructions="""
  Each transaction is a customer's name and an amount in pence (`names[i]` spent `pence[i]`). Write `topSpenders(names, pence, n)`: the `n` customers with the **highest total**, highest first; customers with equal totals are ordered **alphabetically**. If there are fewer than `n` customers, return all of them.

  Totals can be large: add them as `long`. The driver `m3` calls it with hundreds of thousands of transactions, so total with a map rather than searching a list.
  """,
  visible=[("topSpenders", [["ann", "bo", "ann"], [100, 250, 200], 2]), ("topSpenders", [[], [], 3]), ("topSpenders", [["x"], [5], 5])],
  hidden=[("topSpenders", [["b", "a"], [10, 10], 2], "tie broken alphabetically"), ("topSpenders", [["b", "a", "c"], [10, 10, 5], 1], "ties and a limit"), ("m3", [100000, 5], "a hundred thousand customers"), ("m3", [1000, 3], "a thousand customers"), ("m3", [7, 20], "more asked for than exist"), ("topSpenders", [["z", "y", "z"], [1, 5, 4], 3], "totals add up")]),
 dict(id="m4", title="Change request: ids and names ignore case", methods=[("duplicates", [("ids", "List<String>")], "List<String>"), ("topSpenders", [("names", "String[]"), ("pence", "int[]"), ("n", "int")], "List<String>")], fns={"duplicates": dups, "topSpenders": top},
  instructions="""
  **A change request has arrived.** The bank's systems write the same id or name with different capital letters (`T7` and `t7`). They must now count as **the same**. Without breaking milestones 1 to 3:

  - `duplicates` compares ids ignoring case, and reports each in **lower case**.
  - `topSpenders` adds up a customer's spending across all spellings, and reports the name in **lower case**.

  Decide where in your code the one change belongs, and keep it fast.
  """,
  visible=[("duplicates", [["T7", "t7", "A", "a", "a"]]), ("topSpenders", [["Ann", "ann", "Bo"], [100, 100, 150], 2])],
  hidden=[("duplicates", [["Q", "q", "Q"]], "one id in two cases"), ("duplicates", [["a", "B", "b", "A"]], "order by second sighting"), ("topSpenders", [["Ann", "ANN", "bo"], [1, 1, 3], 1], "totals merged across cases"), ("topSpenders", [["B", "a"], [5, 5], 2], "ties after lower-casing"), ("duplicates", [["X", "y"]], "no duplicates")]),
]
rubric = [
 ("Correct and fast", "Fails the large inputs (timeouts or too many reads)", "Passes small cases but one large check is too slow", "Every large check passes: binary search for the range, a hash set for duplicates, a map for totals"),
 ("Choice of structure", "A list is searched repeatedly, or a loop rescans the data for each item", "Mostly the right structures, one avoidable scan remains", "Each job uses the structure that answers its question in constant or logarithmic time"),
 ("Handling the change request", "Milestones 1 to 3 broke, or the case rule was added in several places", "It works, but the lower-casing is repeated in many places", "The rule sits in one place and milestones 1 to 3 still pass"),
 ("Design note", "Missing, or describes the code line by line", "Names the structures but not why", "Explains each cost in big-O terms and why the sorted array and the hash set were the right tools"),
]
project("j5-p1-brightbank", "Brightbank at scale", "B",
    "Search a huge sorted statement, find duplicate ids, and rank customers, within real time limits, then absorb a change request.",
    """
    Brightbank now handles statements with millions of transactions. This stage's tools (binary search, hash sets and maps, sorting) are what make that possible, and the checks will tell you if you chose wrong: they use **large inputs and a time limit**, and for the binary search they **count array reads**.

    You'll write three methods: `countInRange` (how many amounts fall in a range of a sorted statement), `duplicates` (which transaction ids repeat), and `topSpenders` (who spent the most).

    This is an **independent build** with a twist: partway through, a **change request** arrives (milestone 4): ids and names must ignore case. Where you do the lower-casing decides how painful that is.
    """, 5, ["j5-l3.2", "j5-l2.4", "j5-l1.2"], ["J5.02", "J5.06", "J5.10"],
    ["`countInRange` reads only O(log n) elements of the sorted `CountingArray`.",
     "`duplicates` and `topSpenders` handle hundreds of thousands of items in under two seconds.",
     "Totals are added as `long`.",
     "Results follow the orderings stated in each milestone."],
    ["No method scans a list inside a loop over the same data.", "Don't change the drivers."],
    ["Given a sorted array of five million amounts, when the range is counted, then at most about 4 log2(n) elements are read.",
     "Given 200,000 ids with 500 repeats at the end, then `duplicates` returns in time, in order of second sighting.",
     "Given customers with equal totals, then they appear in alphabetical order.",
     "Given the change request, then milestones 1 to 3 still pass unchanged."],
    ms, rubric,
    "In 150 words or fewer: What is the growth rate of each of your three methods, and which structure made it so? Where does your code decide that two ids are the same, and what would you change if the bank said case should matter again?",
    STARTER, SOLUTION, wrongs)

# ======================================================================================= Category C
def top_cat(cats):
    c = Counter(cats)
    return sorted(c, key=lambda k: (-c[k], k))[0] if cats else ""
def m1c(n):
    cats = [f"cat{(i * 7919) % 50:02d}" for i in range(n)]
    return top_cat(cats)
def uniq_sorted(vals):
    return sorted(set(vals))
def m2c(n):
    v = uniq_sorted([int((i * 2654435761) % 100003) for i in range(n)])
    return f"size={len(v)} first={v[0] if v else 0} last={v[-1] if v else 0}"
def m3c(n):
    ids = ",".join(str(i) for i in range(n))
    return f"length={len(ids)} start={ids[:10]} end={ids[-10:] if ids else ''}"
CDRV = '''
// ---------------------------------------------------------------------------------------------
// The report's callers. Don't change them.
// ---------------------------------------------------------------------------------------------

String m1(int n) {
    List<String> categories = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        categories.add(String.format("cat%02d", (int) ((i * 7919L) % 50)));
    }
    return topCategory(categories);
}

String m2(int n) {
    List<Integer> values = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        values.add((int) ((i * 2654435761L) % 100003));
    }
    List<Integer> result = sortedUnique(values);
    return "size=" + result.size() + " first=" + (result.isEmpty() ? 0 : result.get(0)) + " last=" + (result.isEmpty() ? 0 : result.get(result.size() - 1));
}

String m3(int n) {
    List<Integer> ids = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        ids.add(i);
    }
    String joined = joinIds(ids);
    return "length=" + joined.length() + " start=" + joined.substring(0, Math.min(10, joined.length())) + " end=" + (joined.isEmpty() ? "" : joined.substring(Math.max(0, joined.length() - 10)));
}

void main() {
    // Optional: try the report out here.
}
'''
SLOW = '''
// INHERITED CODE: it gives the right answers, and it is far too slow on a real month's data.

// Most common category; if two tie, the alphabetically first.
String topCategory(List<String> categories) {
    String best = "";
    int bestCount = 0;
    for (String category : categories) {
        int count = Collections.frequency(categories, category);
        if (count > bestCount || (count == bestCount && category.compareTo(best) < 0)) {
            best = category;
            bestCount = count;
        }
    }
    return best;
}

// The distinct values, smallest first.
List<Integer> sortedUnique(List<Integer> values) {
    List<Integer> result = new ArrayList<>();
    for (Integer value : values) {
        if (result.contains(value)) {
            continue;
        }
        int position = 0;
        while (position < result.size() && result.get(position) < value) {
            position++;
        }
        result.add(position, value);
    }
    return result;
}

// The ids joined with commas.
String joinIds(List<Integer> ids) {
    String text = "";
    for (int i = 0; i < ids.size(); i++) {
        if (i > 0) {
            text += ",";
        }
        text += ids.get(i);
    }
    return text;
}
'''
FAST = '''
// The most common category; if two tie, the alphabetically first.
String topCategory(List<String> categories) {
    Map<String, Integer> counts = new TreeMap<>();
    for (String category : categories) {
        counts.merge(category, 1, Integer::sum);
    }
    String best = "";
    int bestCount = 0;
    for (Map.Entry<String, Integer> entry : counts.entrySet()) {
        if (entry.getValue() > bestCount) {
            best = entry.getKey();
            bestCount = entry.getValue();
        }
    }
    return best;
}

// The distinct values, smallest first.
List<Integer> sortedUnique(List<Integer> values) {
    return new ArrayList<>(new TreeSet<>(values));
}

// The ids joined with commas.
String joinIds(List<Integer> ids) {
    StringBuilder text = new StringBuilder();
    for (int i = 0; i < ids.size(); i++) {
        if (i > 0) {
            text.append(",");
        }
        text.append(ids.get(i));
    }
    return text.toString();
}
'''
CSOL = FAST + CDRV
CSTART = "// INHERITED slow report. It is correct. The ticket says it must run in under 2 seconds on a month's data.\n// Find where the time goes, and fix it without changing any answer.\n" + SLOW + CDRV
cwrongs = {
  "m1-ties-go-last": CSOL.replace("if (entry.getValue() > bestCount) {", "if (entry.getValue() >= bestCount) {"),
  "m2-keeps-duplicates": CSOL.replace("return new ArrayList<>(new TreeSet<>(values));", "List<Integer> sorted = new ArrayList<>(values);\n    Collections.sort(sorted);\n    return sorted;"),
  "m3-wrong-separator": CSOL.replace('text.append(",");', 'text.append(", ");'),
}
cms = [
 dict(id="m1", title="topCategory is quadratic", methods=[("m1", [("n", "int")], "String")], fns={"m1": m1c},
  instructions="""
  **Ticket:** *"The category report takes over a minute for a month's data (200,000 rows). It must finish in under 2 seconds."*

  `topCategory` returns the most common category (the alphabetically first on a tie). It's correct. Measure it: how many times does `Collections.frequency` scan the list? Fix the cost **without changing any answer**.
  """,
  visible=[(None, [10]), (None, [1]), (None, [0])],
  hidden=[(None, [200000], "a month of rows"), (None, [100000], "half a month"), (None, [49], "fewer rows than categories"), (None, [50], "each category once")]),
 dict(id="m2", title="sortedUnique is quadratic", methods=[("m2", [("n", "int")], "String")], fns={"m2": m2c},
  instructions="""
  **Ticket:** *"The distinct-values step takes minutes for 100,000 numbers."* `sortedUnique` returns the distinct values, smallest first. Find the two avoidable scans inside the loop, and replace the approach, keeping the answer.
  """,
  visible=[(None, [10]), (None, [1]), (None, [0])],
  hidden=[(None, [100000], "a hundred thousand numbers"), (None, [200000], "two hundred thousand"), (None, [5], "five numbers")]),
 dict(id="m3", title="joinIds is quadratic", methods=[("m3", [("n", "int")], "String")], fns={"m3": m3c},
  instructions="""
  **Ticket:** *"Exporting the id list for 200,000 customers never finishes."* `joinIds` returns the ids joined with commas. It is correct. Find out what each `+=` costs, and fix it without changing the output.
  """,
  visible=[(None, [10]), (None, [1]), (None, [0])],
  hidden=[(None, [200000], "two hundred thousand ids"), (None, [100000], "a hundred thousand ids"), (None, [12], "two-digit ids")]),
]
crubric = [
 ("Diagnosis", "Changed code without finding what was slow", "Fixed the slow parts but can't say why they were slow", "Names the cost of each hidden scan (frequency, contains and the insertion loop, string +=) and why it grows with n"),
 ("Evidence", "No measurement before or after", "Measured the final result only", "Measured before and after, or counted steps, and compared with the 2-second requirement"),
 ("Correctness kept", "An answer changed (a tie rule, order or format)", "Answers match except an edge case", "Every answer is identical to the original, including ties, empty input and format"),
 ("Design note", "Missing, or just says it is faster", "Says what was changed", "Explains each growth rate before and after, and what you would measure next"),
]
project("j5-a1-slow-report", "The report that takes a minute", "C",
    "Inherit a correct but far too slow report, find the hidden quadratic costs, and meet a measured time requirement.",
    """
    You've inherited a reporting module. It gives the right answers. It's also so slow on a month of real data that the ticket says nobody can use it. Three methods are the culprits.

    This is not a build; it is a **diagnosis**. For each method, find out what makes it slow (the cost hides inside a library call, not in a visible second loop), fix it, and make sure **no answer changes**: the same tie rules, the same ordering, the same format. The checks run each report on large data under a 2-second limit.

    Don't change the callers (`m1`, `m2`, `m3`). A design note at the end says what you found.
    """, 3, ["j5-l1.2", "j5-l2.4"], ["J5.01", "J5.02", "J5.06"],
    ["Every output is identical to the inherited code's output.",
     "Each report finishes in under 2 seconds on the large input.",
     "Tie rules and ordering are exactly as the original's."],
    ["Don't change the callers.", "Fix the cause, not the symptom: no special-casing of the large inputs."],
    ["Given 200,000 categories, then `topCategory` returns in under 2 seconds with the same answer.",
     "Given 100,000 numbers, then `sortedUnique` returns in time with duplicates removed and values in order.",
     "Given 200,000 ids, then `joinIds` returns the same text in time.",
     "Given equal category counts, then the alphabetically first category is returned."],
    cms, crubric,
    "In 150 words or fewer: For each of the three methods, say what hidden cost made it slow and what its growth rate was before and after. How would you convince a colleague the fix is real?",
    CSTART, CSOL, cwrongs)
print("P7 written")
