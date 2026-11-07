import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-3"
from build import *
import outline, re, calendar, datetime
from decimal import Decimal, ROUND_HALF_UP
from zoneinfo import ZoneInfo
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'
def jd(a, b): return int(a / b)

# ====================================================================== 3.4.1
Lesson("j3-l4.1", "Reading and writing files", ["J3.08"], [
    ("o1", "Write lines to a text file and read them back using Path and Files"),
    ("o2", "Handle a missing or unreadable file by catching IOException"),
    ("o3", "Find and fix a bug where writing replaces the earlier content instead of keeping it"),
], ["j3-l3.3", "j2-l5.3"], 45, ["I34", "I54", "I39"], r'''
## Before you start

You should be comfortable with checked exceptions and try/catch ([Custom and checked exceptions](j2-l5.2), [Cleanup and where to catch](j2-l5.3)), and with lists of strings ([Lists and sets](j3-l1.1)).

**Quick check.** Why must code that reads a file either catch `IOException` or declare `throws IOException`?

<details><summary>Show the answer</summary>

`IOException` is a checked exception, and the compiler requires checked exceptions to be handled or declared.

</details>

## Explanation

### Files and paths

A **`Path`** is the location of a file: `Path.of("data.txt")` or `Path.of("reports", "2026.txt")`. A relative path like these starts from the **current working directory** of the running program, so the same code can look in different places depending on where it's started. The **`Files`** class has static methods that do the actual work `[I34]`.

For small text files, three methods cover most needs:

```java
String text = Files.readString(path);                  // the whole file as one String
List<String> lines = Files.readAllLines(path);         // one String per line
Files.writeString(path, "hello\n");                    // write one String
Files.write(path, lines);                              // write a list of lines, each followed by a newline
```

`readString` decodes the bytes as **UTF-8** `[I54]`, which handles accented letters (`café`) and most other writing systems. Each of these can fail (the file isn't there, the disk is full, you lack permission), so each can throw `IOException`, a checked exception. A method that uses them must declare it or handle it:

```java
void save(Path path, List<String> lines) throws IOException {
    Files.write(path, lines);
}
```

### Writing replaces by default

With no options, writing **creates the file if needed, and truncates an existing one to zero length first** `[I54]`. So writing twice to the same path keeps only the **second** write:

```java
Files.writeString(path, "one\n");
Files.writeString(path, "two\n");     // the file now contains only "two"
```

That's the classic bug in a loop that writes one line at a time. To keep everything you can write all the lines in one call (`Files.write(path, lines)`), or ask for **append** mode:

```java
Files.writeString(path, line + "\n", StandardOpenOption.CREATE, StandardOpenOption.APPEND);
```

Writing everything in one call is simpler and clearer.

### A missing file is an exception, not `null`

Reading a file that doesn't exist throws a `NoSuchFileException`, a kind of `IOException`. Decide what *should* happen and handle it **where you can do something about it**:

```java
String firstLineOr(Path path, String fallback) {
    try {
        List<String> lines = Files.readAllLines(path);
        return lines.isEmpty() ? fallback : lines.get(0);
    } catch (IOException e) {
        return fallback;
    }
}
```

Two cases are handled: a missing file (exception) and an **empty** file (no lines, so `get(0)` would fail). Always ask what an empty or missing input should mean.

### Big files, and resources

`readAllLines` loads the whole file into memory, which is fine for small files. For large ones, `Files.lines(path)` gives a stream that reads lazily, but it holds the file open, so it must be closed: use it in try-with-resources `[I39]`.

### Where to put test files

Programs that write files can easily overwrite something important. The exercises here use a **temporary file** that is created for the check and deleted after. When you write your own tests, do the same instead of using a fixed file name.

## Worked examples

### Example 1: save and load

*Task: save a list of lines to a file, then read them back.*

**Step 1 — Write all lines at once:** `Files.write(path, lines)`.

**Step 2 — Read them back:** `Files.readAllLines(path)`.

**Step 3 — Declare `throws IOException`** on both methods, since both can fail.

```java
void save(Path path, List<String> lines) throws IOException {
    Files.write(path, lines);
}

List<String> load(Path path) throws IOException {
    return Files.readAllLines(path);
}
```

**Step 4 — Check.** After `save(p, List.of("a", "b"))`, `load(p)` is `[a, b]`.

### Example 2: spotting the overwrite

*Task: after saving three lines, `load` returns only the last one. Why?*

```java
for (String line : lines) {
    Files.writeString(path, line + "\n");
}
```

**Step 1 — What does each call do?** It truncates the file, then writes one line.

**Step 2 — So only the last line survives.**

**Step 3 — Fix:** `Files.write(path, lines);`, or add the `APPEND` option to each call.

## Where this is used

- **Configuration, logs, reports and exports** are files read and written by most applications.
- **Data processing scripts** read a file, transform it, and write another.
- **Error handling** around I/O is a daily concern: files go missing, disks fill up.

## Common mistakes

:::mistake{id=MC78}
**Assuming writing adds to the file.** By default it replaces the file's content. Write everything in one call, or use `APPEND`.
:::

:::mistake{id=MC79}
**Forgetting the empty file.** `readAllLines` on an empty file gives an empty list, and `lines.get(0)` then throws. Check for it.
:::

## Practice

::exercise{id=j3-l4.1-write-roundtrip}

::exercise{id=j3-l4.1-write-missing}

::exercise{id=j3-l4.1-debug-overwrite}

## Further reading

- **`java.nio.file.Files`** `[I34]` `[I54]` documents `readString`, `readAllLines`, `write` and the default open options.
- **`java.lang.AutoCloseable`** `[I39]` for try-with-resources with files.

## How you'll be assessed

- The **write** exercises check that you can save and load lines, and handle a missing or empty file (*implementation*).
- The **debug** exercise checks that you can fix a write that overwrites earlier output (*debugging*).
''' + FOOT)

ex = Exercises("j3-l4.1")
RT_DRV = '\n\nString roundTrip(List<String> lines) throws IOException {\n    Path p = Files.createTempFile("academy", ".txt");\n    try {\n        save(p, lines);\n        return String.join("|", load(p));\n    } finally {\n        Files.deleteIfExists(p);\n    }\n}'
RT_SOL = 'void save(Path path, List<String> lines) throws IOException {\n    Files.write(path, lines);\n}\n\nList<String> load(Path path) throws IOException {\n    return Files.readAllLines(path);\n}'
ex.method("write", "j3-l4.1-write-roundtrip", "Save and load lines", ["o1"], ["J3.08"], ["IMPL"],
    "Write `save(Path, List<String>)`, which writes the lines to the file, one per line, and `load(Path)`, which reads them back as a list. The driver `roundTrip` saves to a temporary file, loads, and joins the lines with `|`. Accented letters must survive.",
    [("roundTrip", [("lines", "List<String>")], "String")], {"roundTrip": lambda ls: "|".join(ls)},
    [("roundTrip", [["a", "b", "c"]]), ("roundTrip", [[]]), ("roundTrip", [["only"]])],
    [("roundTrip", [["café", "naïve"]]), ("roundTrip", [["  indented", "trailing  "]]), ("roundTrip", [["a", "", "b"]]), ("roundTrip", [["one line with spaces"]]), ("roundTrip", [["1", "2", "3", "4", "5"]])],
    'void save(Path path, List<String> lines) throws IOException {\n}\n\nList<String> load(Path path) throws IOException {\n    return List.of();\n}' + RT_DRV,
    RT_SOL + RT_DRV,
    {"load-as-one-string": RT_SOL.replace("return Files.readAllLines(path);", "return List.of(Files.readString(path));") + RT_DRV,
     "saves-only-the-first": RT_SOL.replace("Files.write(path, lines);", "if (!lines.isEmpty()) Files.writeString(path, lines.get(0) + \"\\n\");") + RT_DRV},
    ("Files.write(path, lines) writes a list of lines, and Files.readAllLines(path) reads them back. Both can throw IOException.", "Files.write(path, lines); and return Files.readAllLines(path);"),
    difficulty=2)
MISS_DRV = '\n\nString readFirst(String content, boolean fileExists, String fallback) throws IOException {\n    Path p = Files.createTempFile("academy", ".txt");\n    Files.deleteIfExists(p);\n    try {\n        if (fileExists) {\n            Files.writeString(p, content);\n        }\n        return firstLineOr(p, fallback);\n    } finally {\n        Files.deleteIfExists(p);\n    }\n}'
MISS_SOL = 'String firstLineOr(Path path, String fallback) {\n    try {\n        List<String> lines = Files.readAllLines(path);\n        return lines.isEmpty() ? fallback : lines.get(0);\n    } catch (IOException e) {\n        return fallback;\n    }\n}'
def first_line(content, exists, fb):
    if not exists: return fb
    ls = content.splitlines()
    return ls[0] if ls else fb
ex.method("write", "j3-l4.1-write-missing", "A file that might not be there", ["o2"], ["J3.08"], ["IMPL"],
    "Write `firstLineOr(Path path, String fallback)`: return the **first line** of the file, or `fallback` if the file **doesn't exist** or is **empty**. It must not throw. (The driver creates the file, or not, with the content you'd expect.)",
    [("readFirst", [("content", "String"), ("fileExists", "boolean"), ("fallback", "String")], "String")], {"readFirst": first_line},
    [("readFirst", ["hello\nworld", True, "none"]), ("readFirst", ["", False, "none"]), ("readFirst", ["", True, "empty"])],
    [("readFirst", ["only line", True, "x"]), ("readFirst", ["\nsecond", True, "x"]), ("readFirst", ["a\nb\nc", True, "x"]), ("readFirst", ["ignored", False, "missing"]), ("readFirst", ["café\nthé", True, "x"])],
    'String firstLineOr(Path path, String fallback) throws IOException {\n    return Files.readAllLines(path).get(0);\n}' + MISS_DRV,
    MISS_SOL + MISS_DRV,
    {"no-catch": MISS_SOL.replace("    try {\n        List<String> lines = Files.readAllLines(path);\n        return lines.isEmpty() ? fallback : lines.get(0);\n    } catch (IOException e) {\n        return fallback;\n    }", "    List<String> lines = Files.readAllLines(path);\n    return lines.isEmpty() ? fallback : lines.get(0);").replace("String firstLineOr(Path path, String fallback) {", "String firstLineOr(Path path, String fallback) throws IOException {") + MISS_DRV,
     "crashes-on-empty": MISS_SOL.replace("lines.isEmpty() ? fallback : lines.get(0)", "lines.get(0)") + MISS_DRV},
    ("Two things can go wrong: reading throws IOException when the file is missing, and an empty file has no first line.", "try { List<String> lines = Files.readAllLines(path); return lines.isEmpty() ? fallback : lines.get(0); } catch (IOException e) { return fallback; }"),
    source_tests=[("catches IOException", ["catch (IOException"], None)],
    difficulty=3)
OW_BAD = 'void save(Path path, List<String> lines) throws IOException {\n    for (String line : lines) {\n        Files.writeString(path, line + "\\n");\n    }\n}\n\nList<String> load(Path path) throws IOException {\n    return Files.readAllLines(path);\n}'
ex.method("debug", "j3-l4.1-debug-overwrite", "Only the last line survives", ["o3"], ["J3.08"], ["DEBUG"],
    "`roundTrip` saves some lines and loads them back, but only the **last** line comes back. Find out why, and fix `save` so that all the lines are kept (in order).",
    [("roundTrip", [("lines", "List<String>")], "String")], {"roundTrip": lambda ls: "|".join(ls)},
    [("roundTrip", [["a", "b", "c"]]), ("roundTrip", [[]]), ("roundTrip", [["only"]])],
    [("roundTrip", [["x", "y"]]), ("roundTrip", [["one", "two", "three", "four"]]), ("roundTrip", [["café", "thé"]]), ("roundTrip", [["a", "", "b"]]), ("roundTrip", [["last", "first"]])],
    OW_BAD + RT_DRV,
    RT_SOL + RT_DRV,
    {"append-without-newline": 'void save(Path path, List<String> lines) throws IOException {\n    for (String line : lines) {\n        Files.writeString(path, line, StandardOpenOption.CREATE, StandardOpenOption.APPEND);\n    }\n}\n\nList<String> load(Path path) throws IOException {\n    return Files.readAllLines(path);\n}' + RT_DRV},
    ("What does Files.writeString do to a file that already has content? What happens on the second line?", "Write all the lines in one call: Files.write(path, lines);"),
    difficulty=3)
reg({"j3-l4.1": ("Reading and writing files", ["J3.08"])},
    {"MC78": (["J3.08"], "I54", "Writing to a file with Files.writeString adds to what is there"),
     "MC79": (["J3.08"], "Platform", "Reading an empty file gives one empty line, or null")})

# ====================================================================== 3.4.2
Lesson("j3-l4.2", "Parsing text data and handling failures", ["J3.09"], [
    ("o1", "Split lines of delimited text into fields and convert them to values"),
    ("o2", "Validate each line, count or collect the bad ones, and keep going"),
    ("o3", "Explain why data from outside the program has to be checked, and what a good report of bad data contains"),
], ["j3-l4.1"], 45, ["I49", "I34", "R16"], r'''
## Before you start

You should be able to read lines from a file ([Reading and writing files](j3-l4.1)) and use a map to total things ([Maps](j3-l1.2)).

**Quick check.** What exception does `Integer.parseInt("abc")` throw?

<details><summary>Show the answer</summary>

`NumberFormatException`.

</details>

## Explanation

### Data from outside is not trustworthy

A file, a form, a network message or a spreadsheet export can contain **anything**: blank lines, missing fields, a header row, text where a number should be, an extra comma, a stray space. A program that assumes tidy input will crash on the first untidy line, usually in the middle of a long job.

The professional habit: **parse defensively.** For each line, check it, use it if it's good, and **record** it if it's bad, so that one bad row doesn't ruin the rest, and the person can find the bad rows afterwards.

### CSV: lines of comma-separated values

A very common format is **CSV** (comma-separated values): one record per line, fields separated by commas, perhaps a header row first:

```
category,amount
food,1250
rent,50000
food,
```

You split a line into fields with `split`:

```java
String[] parts = line.split(",");
```

`split` takes a *regular expression* (a pattern; a plain comma is also a pattern that matches a comma). It has a gotcha: **it discards trailing empty strings** unless you give a negative limit `[I49]`:

```java
"a,b,,".split(",")        // ["a", "b"]        (the empty trailing fields are dropped)
"a,b,,".split(",", -1)    // ["a", "b", "", ""] (all four fields kept)
```

For data where an empty last field means something (here: a missing amount), use `split(",", -1)` so the number of fields is what the line really has. Real CSV can also have quoted fields containing commas (`"Smith, John"`); that needs a proper CSV library, which is why this lesson sticks to the simple kind.

### Validating a line

For each line, decide what counts as good, and test it in a sensible order:

1. **Skip what isn't data:** blank lines and the header.
2. **Count the fields.** Wrong number of fields means a bad line.
3. **Strip** each field of spaces (`strip()` removes spaces from both ends).
4. **Check each field:** a category mustn't be empty; an amount must be digits.
5. **Convert**, and only then use it.

To check that text is all digits without risking an exception, `text.matches("[0-9]+")` tests it against a pattern: one or more digits. (Negative numbers and decimals would need a longer pattern.) Alternatively, call `Integer.parseInt` inside try/catch and treat `NumberFormatException` as "bad".

```java runnable
void main() {
    String[] lines = { "category,amount", "food,1250", "rent,50000", "food,", "", "food, 750 " };
    Map<String, Integer> totals = new TreeMap<>();
    int bad = 0;
    for (String raw : lines) {
        String line = raw.strip();
        if (line.isEmpty() || line.equalsIgnoreCase("category,amount")) {
            continue;
        }
        String[] parts = line.split(",", -1);
        if (parts.length != 2) {
            bad++;
            continue;
        }
        String category = parts[0].strip();
        String amount = parts[1].strip();
        if (category.isEmpty() || !amount.matches("[0-9]+")) {
            bad++;
            continue;
        }
        totals.merge(category, Integer.parseInt(amount), Integer::sum);
    }
    IO.println(totals + " bad=" + bad);
}
```

It prints `{food=2000, rent=50000} bad=1`. The line `food,` is the bad one: two fields, but the amount is empty. `food, 750 ` is fine, once stripped.

### Reporting problems usefully

Counting bad lines is a start. A good report says **which** lines and **why**, so the person can fix them:

- the **line number** (in a file, count from 1) and the line's text;
- what was wrong ("amount isn't a number");
- the totals for what *was* good, clearly separated.

Decide too whether bad data should stop the job (a payroll run probably should) or be skipped and reported (a log analysis probably should). That's a requirement question, not a coding one.

## Worked examples

### Example 1: how many fields?

*Task: `"a,b,"` should count as 3 fields (the last one is empty).*

**Step 1 — What does the plain `split(",")` give?** `["a", "b"]`, which is 2.

**Step 2 — Use the negative limit:** `split(",", -1)` gives `["a", "b", ""]`, which is 3.

**Step 3 — Check.** `countFields("a,b,")` is 3.

### Example 2: skip, don't crash

*Task: total the amounts, ignoring lines that aren't valid.*

**Step 1 — Check before converting,** so no exception is needed.

**Step 2 — Count what you skip.**

**Step 3 — Return both the total and the number skipped,** so the caller knows data was dropped.

## Where this is used

- **Import and export:** bank statements, spreadsheets and logs arrive as CSV or text.
- **Pipelines and ETL jobs** process millions of lines; one bad line must not stop them.
- **Security:** treating all outside input as hostile is the first rule of safe software.

## Common mistakes

:::mistake{id=MC80}
**Using `split(",")` and expecting trailing empty fields.** They're dropped. Use `split(",", -1)`.
:::

:::mistake{id=MC81}
**Assuming the data is well-formed.** The first blank line, header or stray space breaks code that assumes tidiness.
:::

## Practice

::exercise{id=j3-l4.2-write-summarise}

::exercise{id=j3-l4.2-debug-fields}

::exercise{id=j3-l4.2-explain-trust}

## Further reading

- **`java.lang.String`** `[I49]` documents `split` and its limit parameter.
- **`java.nio.file.Files`** `[I34]` for reading the lines in the first place.
- **McCauley et al. (2008)** `[R16]` on debugging: a failing run on real data is a test case, so keep the lines that broke your code.

## How you'll be assessed

- The **write** exercise checks that you can parse, validate and total lines and count the bad ones (*implementation*).
- The **debug** exercise checks that you know `split` drops trailing empty strings (*debugging*).
- The **explain** exercise checks that you can say why input must be validated and what to report (*explanation*).
''' + FOOT)

ex = Exercises("j3-l4.2")
def summarise(lines):
    tot, bad = {}, 0
    for raw in lines:
        line = raw.strip()
        if line == "" or line.lower() == "category,amount": continue
        parts = line.split(",")
        if len(parts) != 2: bad += 1; continue
        c, a = parts[0].strip(), parts[1].strip()
        if c == "" or not re.fullmatch(r"[0-9]+", a): bad += 1; continue
        tot[c] = tot.get(c, 0) + int(a)
    body = ",".join(f"{k}={tot[k]}" for k in sorted(tot)) or "none"
    return f"{body} | bad={bad}"
SUM_SOL = 'String summarise(List<String> lines) {\n    Map<String, Integer> totals = new TreeMap<>();\n    int bad = 0;\n    for (String raw : lines) {\n        String line = raw.strip();\n        if (line.isEmpty() || line.equalsIgnoreCase("category,amount")) {\n            continue;\n        }\n        String[] parts = line.split(",", -1);\n        if (parts.length != 2) {\n            bad++;\n            continue;\n        }\n        String category = parts[0].strip();\n        String amount = parts[1].strip();\n        if (category.isEmpty() || !amount.matches("[0-9]+")) {\n            bad++;\n            continue;\n        }\n        totals.merge(category, Integer.parseInt(amount), Integer::sum);\n    }\n    StringBuilder out = new StringBuilder();\n    for (Map.Entry<String, Integer> e : totals.entrySet()) {\n        if (!out.isEmpty()) out.append(",");\n        out.append(e.getKey()).append("=").append(e.getValue());\n    }\n    return (out.isEmpty() ? "none" : out) + " | bad=" + bad;\n}'
ex.method("write", "j3-l4.2-write-summarise", "Totals from messy lines", ["o1", "o2"], ["J3.09"], ["IMPL"],
    "Each line should be `category,amount` (amount a whole number of pence, not negative). Write `summarise(List<String> lines)` so that it **skips** blank lines and the header line `category,amount` (any case), counts as **bad** any other line that doesn't have exactly two fields, an empty category, or an amount that isn't digits, and ignores spaces around fields. It returns the totals per category, **sorted by category**, as `food=2000,rent=50000`, then ` | bad=` and the number of bad lines. If no line was good, the totals part is `none`.",
    [("summarise", [("lines", "List<String>")], "String")], {"summarise": summarise},
    [("summarise", [["category,amount", "food,1250", "rent,50000", "food,", "", "food, 750 "]]), ("summarise", [[]]), ("summarise", [["a,1", "a,2"]])],
    [("summarise", [["x,-5", "y,12.5", "z,abc"]]), ("summarise", [[",100", "a,b,c", "just text"]]), ("summarise", [["  tea , 300 ", "TEA,200"]]), ("summarise", [["CATEGORY,AMOUNT", "pear,5"]]), ("summarise", [["", "   ", "\t"]]), ("summarise", [["b,2", "a,1", "c,3", "a,4"]])],
    'String summarise(List<String> lines) {\n    return "";\n}',
    SUM_SOL,
    {"allows-negative": SUM_SOL.replace('"[0-9]+"', '"-?[0-9]+"'),
     "does-not-strip": SUM_SOL.replace("String amount = parts[1].strip();", "String amount = parts[1];"),
     "blank-lines-are-bad": SUM_SOL.replace("if (line.isEmpty() || line.equalsIgnoreCase", "if (line.equalsIgnoreCase").replace("        String[] parts = line.split", "        if (line.isEmpty()) { bad++; continue; }\n        String[] parts = line.split")},
    ("Work through each line: skip, count fields (split with -1), strip, check, then total with a TreeMap.", "line.split(\",\", -1); parts.length != 2 -> bad; !amount.matches(\"[0-9]+\") -> bad; totals.merge(category, n, Integer::sum)"),
    difficulty=4)
ex.method("debug", "j3-l4.2-debug-fields", "The missing last field", ["o2"], ["J3.09"], ["DEBUG"],
    "`countFields(line)` should return how many comma-separated fields a line has, **including empty ones**: `\"a,b,c\"` has 3, and `\"a,b,\"` also has 3 (the last is empty). It says 2 for `\"a,b,\"`. Find out why and fix it.",
    [("countFields", [("line", "String")], "int")], {"countFields": lambda s: len(s.split(","))},
    [("countFields", ["a,b,c"]), ("countFields", ["a,b,"]), ("countFields", ["a"])],
    [("countFields", [""]), ("countFields", [",,"]), ("countFields", ["x,,z"]), ("countFields", [",a"]), ("countFields", ["one,two,three,four,"])],
    'int countFields(String line) {\n    return line.split(",").length;\n}',
    'int countFields(String line) {\n    return line.split(",", -1).length;\n}',
    {"counts-commas-only": 'int countFields(String line) {\n    int n = 0;\n    for (char c : line.toCharArray()) {\n        if (c == \',\') n++;\n    }\n    return n;\n}'},
    ("What does split(\",\") do with empty fields at the end?", "Use split(\",\", -1) so trailing empty fields are kept."),
    difficulty=2)
ex.explain("j3-l4.2-explain-trust", "Why check the data?", ["o3"], ["J3.09"],
    "A teammate's import code does `Integer.parseInt(line.split(\",\")[1])` for every line of a customer's CSV, and it crashes at line 4,031 of 10,000. (a) Give three kinds of bad line that could cause a crash like this. (b) Say what the code should do about a bad line, instead of crashing. (c) Say what the person who supplied the file needs to be told.",
    "A full answer lists three kinds of bad line (a header row, a blank line, a missing field or non-numeric amount, an extra comma) and says the code should validate each line, skip the bad ones and carry on, and then report which lines (line numbers and reasons) were rejected, alongside what was imported.",
    {2: ("Gives three kinds of bad line (such as a header, a blank line, a missing or text amount, a stray comma), says to validate and skip while continuing, and says to report which lines were rejected with line numbers and reasons.",
         ["A header row, a blank line, and a line with a missing or non-numeric amount like \"food,\" or \"food,abc\" could all crash it. The code should check each line, skip the bad ones and keep going. Then it should report the rejected lines, with line numbers and why, as well as what was imported, so the customer can fix them.",
          "Blank lines, a header, and a line with too few fields or text where a number should be. The importer should validate each line and skip the bad ones instead of crashing. The customer should be told the line numbers and the problem with each rejected line."]),
     1: ("Names some bad lines and says to validate, but doesn't say how to report them, or the reverse.",
         ["A blank line could crash it. Check the lines first.", "Tell them which lines failed."]),
     0: ("Incorrect, for example says the file is simply wrong and the program should be allowed to crash.",
         ["The customer's file is wrong so it's fine to crash.", "Catch Exception and ignore it."])})
reg({"j3-l4.2": ("Parsing text data and handling failures", ["J3.09"])},
    {"MC80": (["J3.09"], "I49", "split(\",\") keeps empty fields at the end of a line"),
     "MC81": (["J3.09"], "Platform", "Input files are always tidy and well-formed")})

# ====================================================================== 3.5.1
Lesson("j3-l5.1", "Dates and time zones", ["J3.10"], [
    ("o1", "Choose between LocalDate, LocalDateTime, Instant and ZonedDateTime for a given need"),
    ("o2", "Do date arithmetic and formatting with java.time, including days between dates"),
    ("o3", "Avoid daylight-saving mistakes by adding days or hours deliberately"),
], ["j3-l4.2", "j2-l4.1"], 50, ["I33", "I44", "I45", "I51", "R16"], r'''
## Before you start

You should know immutability and value types ([Immutability and defensive copies](j2-l2.2), [Records and enums](j2-l4.1)). The `java.time` classes are all immutable values.

**Quick check.** If `d` is a `LocalDate` and you call `d.plusDays(1)`, does `d` change?

<details><summary>Show the answer</summary>

No. `java.time` objects are immutable; `plusDays` returns a **new** `LocalDate`.

</details>

## Explanation

Dates and times look simple until the clocks change. The `java.time` package, which compact source files can use without an import, gives you separate types for separate ideas. Choosing the right one avoids most bugs.

### Four types to tell apart

| Type | What it is | Example | Use for |
|---|---|---|---|
| `LocalDate` | a date, **no time, no zone** `[I33]` | `2026-11-06` | birthdays, due dates, statement dates |
| `LocalDateTime` | a date **and** time, **no zone** | `2026-11-06T09:30` | a wall-clock time whose zone is known elsewhere |
| `Instant` | one exact moment on the time-line `[I33]` | `2026-11-06T09:30:00Z` | timestamps, event logs, "when did it happen" |
| `ZonedDateTime` | date, time **and** a time-zone `[I33]` | `2026-11-06T09:30+00:00[Europe/London]` | showing a moment to a person in their zone |

`LocalDateTime` doesn't identify a moment: "9:30 on 6 November" means a different instant in London and in Tokyo. A `ZonedDateTime` (or an `Instant`) does.

**A good rule:** store and compare **moments** as `Instant` (the same everywhere); convert to a `ZonedDateTime` in the user's zone only to **show** them; use `LocalDate` for things that really are calendar dates.

### Making and reading them

```java
LocalDate d = LocalDate.parse("2026-11-06");                       // ISO format yyyy-MM-dd
LocalDate due = d.plusDays(30);
d.getDayOfWeek();                                                  // FRIDAY
d.lengthOfMonth();                                                 // 30
d.withDayOfMonth(1);                                               // 2026-11-01
d.isBefore(due);                                                   // true
long days = ChronoUnit.DAYS.between(d, due);                       // 30
```

`LocalDate`'s methods include `plusDays`, `minusDays`, `lengthOfMonth`, `getDayOfWeek`, `isLeapYear` and `parse`, and `ChronoUnit.DAYS.between(a, b)` counts the days from `a` to `b` (negative if `b` is earlier) `[I51]`. Parsing text that isn't a valid date throws a `DateTimeParseException`.

### Formatting

`DateTimeFormatter` turns dates into text and back `[I45]`:

```java
DateTimeFormatter f = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");
String text = LocalDateTime.of(2026, 11, 6, 9, 30).format(f);     // "06/11/2026 09:30"
```

In patterns, `MM` is the month and `mm` is minutes; `HH` is the hour on a 24-hour clock. Mixing up `MM` and `mm` is a very common mistake. Always give a pattern explicitly rather than relying on defaults that vary by region.

### Time zones

A **`ZoneId`** names a time-zone, such as `Europe/London`, `America/New_York`, `Asia/Tokyo`; the zone knows its own daylight-saving rules `[I45]`. To show a moment in another zone, use `withZoneSameInstant`:

```java
ZonedDateTime london = ZonedDateTime.of(LocalDateTime.of(2026, 7, 1, 12, 0), ZoneId.of("Europe/London"));
ZonedDateTime tokyo = london.withZoneSameInstant(ZoneId.of("Asia/Tokyo"));   // same instant, different clock
```

**Don't use fixed hour offsets as time-zones** (`+01:00`): they don't change with daylight saving.

### The daylight-saving trap: a day is not always 24 hours

When the clocks go forward, one day has 23 hours; when they go back, one has 25. So:

- **`Duration`** is an amount of **exact time** (hours, seconds). Its DAYS unit is *exactly* 24 hours, and it ignores daylight saving `[I44]`.
- **`Period`** is an amount of **calendar time** (days, months, years) `[I44]`.

Adding to a `ZonedDateTime` shows the difference:

```java
ZonedDateTime before = ZonedDateTime.of(LocalDateTime.of(2026, 3, 28, 12, 0), ZoneId.of("Europe/London"));
before.plusHours(24);    // 2026-03-29T13:00+01:00[Europe/London]   (the clocks went forward in between)
before.plusDays(1);      // 2026-03-29T12:00+01:00[Europe/London]   (the same clock time, next day)
```

On 29 March 2026 the clocks in London went forward an hour, so 24 hours after noon on the 28th is 1 pm on the 29th. "Same time tomorrow" is `plusDays(1)`. Pick the one that matches what the requirement **means**: a statement due "in 24 hours" is a duration; a rent payment due "the same time tomorrow" is a day.

## Worked examples

### Example 1: days between two dates

*Task: how many days from 1 March to 1 April 2026?*

**Step 1 — Both are dates with no time:** `LocalDate`.

**Step 2 — Count with `ChronoUnit.DAYS.between`:**

```java runnable
void main() {
    LocalDate from = LocalDate.parse("2026-03-01");
    LocalDate to = LocalDate.parse("2026-04-01");
    IO.println(ChronoUnit.DAYS.between(from, to));
    IO.println(ChronoUnit.DAYS.between(to, from));
}
```

It prints `31` and `-31`.

### Example 2: the last working day of the month

*Task: the last Monday-to-Friday day of the month containing a date.*

**Step 1 — Start at the last day of the month:** `d.withDayOfMonth(d.lengthOfMonth())`.

**Step 2 — Step back while it's a weekend:**

```java
String lastWeekday(String date) {
    LocalDate d = LocalDate.parse(date);
    LocalDate last = d.withDayOfMonth(d.lengthOfMonth());
    while (last.getDayOfWeek() == DayOfWeek.SATURDAY || last.getDayOfWeek() == DayOfWeek.SUNDAY) {
        last = last.minusDays(1);
    }
    return last.toString();
}
```

**Step 3 — Check.** If a month ends on a Saturday, it steps back to Friday. `LocalDate.toString()` gives the ISO form.

## Where this is used

- **Statements, deadlines, subscriptions and schedules** are all date arithmetic.
- **Logging and auditing** use `Instant` so timestamps from different servers agree.
- **Anything with users in different countries** shows moments in each person's own zone.

## Common mistakes

:::mistake{id=MC82}
**Adding 24 hours when you mean "one day".** On a day when the clocks change, `plusHours(24)` and `plusDays(1)` give different clock times.
:::

:::mistake{id=MC83}
**Treating a `LocalDateTime` as a moment in time.** It has no zone, so it doesn't say when something happened. Use an `Instant` or a `ZonedDateTime`.
:::

:::mistake{id=MC84}
**Writing `mm` for the month.** `MM` is the month and `mm` is minutes.
:::

## Practice

::exercise{id=j3-l5.1-write-weekday}

::exercise{id=j3-l5.1-write-days}

::exercise{id=j3-l5.1-debug-zone}

::exercise{id=j3-l5.1-explain-instant}

## Further reading

- **`java.time`: `LocalDate`, `Instant`, `ZonedDateTime`** `[I33]` and the method names in `[I51]`.
- **`Duration` and `Period`** `[I44]` explain the daylight-saving difference.
- **`DateTimeFormatter` and `ZoneId`** `[I45]`.
- **McCauley et al. (2008)** `[R16]` on debugging: bugs that depend on the date need tests on the specific dates that trigger them.

## How you'll be assessed

- The **write** exercises check that you can do date arithmetic with `LocalDate` and `ChronoUnit` (*implementation*).
- The **debug** exercise checks that you can fix a daylight-saving bug (*debugging*).
- The **explain** exercise checks that you can choose the right type for storing and showing a moment (*explanation*).
''' + FOOT)

ex = Exercises("j3-l5.1")
def last_weekday(s):
    d = datetime.date.fromisoformat(s)
    last = datetime.date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])
    while last.weekday() >= 5: last -= datetime.timedelta(days=1)
    return last.isoformat()
LW_SOL = 'String lastWeekday(String date) {\n    LocalDate d = LocalDate.parse(date);\n    LocalDate last = d.withDayOfMonth(d.lengthOfMonth());\n    while (last.getDayOfWeek() == DayOfWeek.SATURDAY || last.getDayOfWeek() == DayOfWeek.SUNDAY) {\n        last = last.minusDays(1);\n    }\n    return last.toString();\n}'
ex.method("write", "j3-l5.1-write-weekday", "The last working day", ["o2"], ["J3.10"], ["IMPL"],
    "Write `lastWeekday(String date)`: given a date such as `2026-10-15` (`yyyy-MM-dd`), return the **last weekday** (Monday to Friday) of that date's month, in the same format. If the month ends on a weekend, go back to the Friday.",
    [("lastWeekday", [("date", "String")], "String")], {"lastWeekday": last_weekday},
    [("lastWeekday", ["2026-10-15"]), ("lastWeekday", ["2026-11-06"]), ("lastWeekday", ["2026-02-01"])],
    [("lastWeekday", ["2026-05-20"]), ("lastWeekday", ["2024-02-10"]), ("lastWeekday", ["2025-08-01"]), ("lastWeekday", ["2026-01-31"]), ("lastWeekday", ["2023-12-25"]), ("lastWeekday", ["2027-04-30"])],
    'String lastWeekday(String date) {\n    return date;\n}',
    LW_SOL,
    {"stops-at-last-day": LW_SOL.replace("while (last.getDayOfWeek() == DayOfWeek.SATURDAY || last.getDayOfWeek() == DayOfWeek.SUNDAY) {\n        last = last.minusDays(1);\n    }\n", ""),
     "goes-forward": LW_SOL.replace("last = last.minusDays(1);", "last = last.plusDays(1);").replace("last = d.withDayOfMonth(d.lengthOfMonth())", "last = d.withDayOfMonth(d.lengthOfMonth())")},
    ("Start at the last day of the month (withDayOfMonth(lengthOfMonth())), and step back while the day is a Saturday or Sunday.", "while (weekend) { last = last.minusDays(1); }"),
    difficulty=3)
ex.method("write", "j3-l5.1-write-days", "Days between two dates", ["o2"], ["J3.10"], ["IMPL"],
    "Write `daysBetween(String from, String to)`: the number of days from the first date to the second (`yyyy-MM-dd`). It is **negative** if the second date is earlier. Use `java.time`, not your own calendar arithmetic.",
    [("daysBetween", [("from", "String"), ("to", "String")], "long")],
    {"daysBetween": lambda a, b: (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days},
    [("daysBetween", ["2026-03-01", "2026-04-01"]), ("daysBetween", ["2026-04-01", "2026-03-01"]), ("daysBetween", ["2026-05-05", "2026-05-05"])],
    [("daysBetween", ["2024-02-28", "2024-03-01"]), ("daysBetween", ["2025-02-28", "2025-03-01"]), ("daysBetween", ["2026-01-01", "2027-01-01"]), ("daysBetween", ["2000-01-01", "2026-11-06"]), ("daysBetween", ["2026-12-31", "2026-01-01"])],
    'long daysBetween(String from, String to) {\n    return 0;\n}',
    'long daysBetween(String from, String to) {\n    return ChronoUnit.DAYS.between(LocalDate.parse(from), LocalDate.parse(to));\n}',
    {"reversed": 'long daysBetween(String from, String to) {\n    return ChronoUnit.DAYS.between(LocalDate.parse(to), LocalDate.parse(from));\n}',
     "months-times-thirty": 'long daysBetween(String from, String to) {\n    LocalDate a = LocalDate.parse(from);\n    LocalDate b = LocalDate.parse(to);\n    return (b.getYear() - a.getYear()) * 365L + (b.getMonthValue() - a.getMonthValue()) * 30L + (b.getDayOfMonth() - a.getDayOfMonth());\n}'},
    ("ChronoUnit.DAYS.between(a, b) counts from a to b. Parse the text into LocalDate values first.", "ChronoUnit.DAYS.between(LocalDate.parse(from), LocalDate.parse(to))"),
    source_tests=[("uses java.time", ["ChronoUnit"], None)],
    difficulty=2)
def next_day(local, zone):
    tz = ZoneInfo(zone)
    d = datetime.datetime.fromisoformat(local) + datetime.timedelta(days=1)
    return d.strftime("%Y-%m-%d %H:%M")
ZONE_BAD = 'String nextDaySameTime(String local, String zone) {\n    ZonedDateTime start = ZonedDateTime.of(LocalDateTime.parse(local), ZoneId.of(zone));\n    ZonedDateTime next = start.plus(Duration.ofHours(24));\n    return next.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));\n}'
ZONE_OK = ZONE_BAD.replace("start.plus(Duration.ofHours(24))", "start.plusDays(1)")
ex.method("debug", "j3-l5.1-debug-zone", "The day that was 23 hours long", ["o3"], ["J3.10"], ["DEBUG"],
    "`nextDaySameTime(\"2026-03-28T12:00\", \"Europe/London\")` should return the **same clock time on the next day**: `2026-03-29 12:00`. It returns `13:00`, because the clocks in London go forward on 29 March 2026. Find the cause and fix it. (All the checks use midday times, so you needn't worry about clock times that don't exist.)",
    [("nextDaySameTime", [("local", "String"), ("zone", "String")], "String")], {"nextDaySameTime": next_day},
    [("nextDaySameTime", ["2026-03-28T12:00", "Europe/London"]), ("nextDaySameTime", ["2026-06-10T12:00", "Europe/London"]), ("nextDaySameTime", ["2026-03-07T12:00", "America/New_York"])],
    [("nextDaySameTime", ["2026-10-24T12:00", "Europe/London"]), ("nextDaySameTime", ["2026-11-01T12:00", "America/New_York"]), ("nextDaySameTime", ["2026-01-15T12:00", "Asia/Tokyo"]), ("nextDaySameTime", ["2026-03-28T12:00", "Europe/Paris"]), ("nextDaySameTime", ["2026-12-31T12:00", "Europe/London"])],
    ZONE_BAD, ZONE_OK,
    {"converts-to-utc": ZONE_OK.replace("return next.format(", "return next.withZoneSameInstant(ZoneId.of(\"UTC\")).format("),
     "adds-a-month": ZONE_OK.replace("start.plusDays(1)", "start.plusMonths(1)")},
    ("What is the difference between adding 24 hours and adding one day, on the day the clocks change?", "Use start.plusDays(1), which keeps the same clock time."),
    difficulty=3)
ex.explain("j3-l5.1-explain-instant", "Which type?", ["o1"], ["J3.10"],
    "For each, say which of `LocalDate`, `LocalDateTime`, `Instant` and `ZonedDateTime` fits best, and why: (a) the moment an order was placed, stored in a database used by servers in several countries; (b) a customer's date of birth; (c) showing that order time to a customer in Tokyo; (d) \"the meeting is at 9:30 on 14 May\", before anyone has said whose time-zone it's in.",
    "A full answer chooses Instant for the order moment (a single exact point that's the same everywhere), LocalDate for the date of birth (a calendar date with no time or zone), ZonedDateTime for showing it in Tokyo (the instant converted to the customer's zone), and LocalDateTime for the unzoned meeting time.",
    {2: ("Gives Instant for (a), LocalDate for (b), ZonedDateTime for (c) and LocalDateTime for (d), each with a correct reason about moments, zones and calendar dates.",
         ["(a) Instant: it's one exact moment, the same in every country. (b) LocalDate: a calendar date needs no time or zone. (c) ZonedDateTime, converting the instant to Asia/Tokyo for display. (d) LocalDateTime: it has a date and time but no zone yet.",
          "Instant for the order time, LocalDate for the birth date, ZonedDateTime to show it in Tokyo, and LocalDateTime for the meeting before a zone is decided."]),
     1: ("Gets two or three right, or gives choices without reasons.",
         ["(a) Instant (b) LocalDate (c) LocalDateTime (d) ZonedDateTime", "Use ZonedDateTime for everything."]),
     0: ("Incorrect, for example uses LocalDateTime for the order moment or says a time-zone isn't needed.",
         ["LocalDateTime for all of them.", "Zones are not important."])})
reg({"j3-l5.1": ("Dates and time zones", ["J3.10"])},
    {"MC82": (["J3.10"], "I44", "plusHours(24) and plusDays(1) always give the same clock time"),
     "MC83": (["J3.10"], "I33", "A LocalDateTime identifies a single moment in time"),
     "MC84": (["J3.10"], "Platform", "mm in a date pattern means the month")})

# ====================================================================== 3.5.2
Lesson("j3-l5.2", "Money and BigDecimal", ["J3.11"], [
    ("o1", "Explain why a double isn't suitable for money, using a concrete example"),
    ("o2", "Calculate with BigDecimal using an explicit scale and RoundingMode, or with whole pence, and share a total without losing a penny"),
    ("o3", "Compare BigDecimal values correctly with compareTo and not equals"),
], ["j3-l5.1"], 50, ["I32", "I48", "I46", "R16"], r'''
## Before you start

You've used whole pence as `int` for money since Stage 1 ([Arithmetic: division, remainders and exact results](j1-l2.3)), and you know immutability ([Immutability and defensive copies](j2-l2.2)).

**Quick check.** Why did the earlier projects store `£12.34` as `1234`?

<details><summary>Show the answer</summary>

Whole numbers of pence are exact; fractions of a pound in `double` aren't.

</details>

## Explanation

### Why `double` is wrong for money

A `double` stores numbers in binary, and many ordinary decimal numbers have no exact binary form, just as 1/3 has no exact decimal form. Run this:

```java runnable
void main() {
    IO.println(0.1 + 0.2);
    IO.println(0.1 + 0.2 == 0.3);
}
```

It prints `0.30000000000000004` and `false`. For graphics or physics those tiny errors don't matter. For money, they accumulate, and they make `==` unreliable: a bill total might be off by a hundred-millionth of a penny and refuse to match.

There are two good ways to handle money.

### Way 1: whole units (what you've been doing)

Store money as an `int` or `long` count of the smallest unit, such as pence. Addition and subtraction are exact. The things to design are **division and percentages**, because they produce fractions that must go somewhere:

```java
int vat = price * 20 / 100;      // rounds down: 1999 * 20 / 100 is 399, not 399.8
```

You must decide the rounding rule on purpose (down, half-up, ...) and write it in one place.

**Sharing a total without losing pennies.** Splitting 1000 pence among 3 people gives 333 each, which loses 1 penny. Give the leftover to the first few:

```java
List<Integer> split(int total, int people) {
    List<Integer> shares = new ArrayList<>();
    for (int i = 0; i < people; i++) {
        shares.add(total / people + (i < total % people ? 1 : 0));
    }
    return shares;      // 1000 among 3: [334, 333, 333], and the shares add up to 1000
}
```

### Way 2: `BigDecimal`

`BigDecimal` stores a decimal number exactly, as digits and a **scale** (how many digits after the point) `[I32]`. It's immutable: every operation returns a **new** object `[I32]`.

```java
BigDecimal a = new BigDecimal("0.1");     // build from a String, never from a double
BigDecimal b = new BigDecimal("0.2");
a.add(b);                                  // 0.3 exactly
```

**Create `BigDecimal` from a `String`**, not from a `double`: `new BigDecimal(0.1)` starts from the already-inexact binary value.

The operations: `add`, `subtract`, `multiply`, `divide`, `negate`, `max`, `min`. **Division** can fail: dividing 1 by 3 has no exact decimal answer, so `divide` throws an `ArithmeticException` unless you say how many digits to keep and how to round:

```java
BigDecimal third = BigDecimal.ONE.divide(new BigDecimal("3"), 4, RoundingMode.HALF_UP);   // 0.3333
```

`RoundingMode` has constants such as `UP`, `DOWN`, `HALF_UP`, `HALF_DOWN`, `HALF_EVEN`, `CEILING`, `FLOOR` `[I46]`. `HALF_UP` is what most people mean by "round": 2.5 becomes 3. Finish a money calculation with an explicit `setScale`:

```java
BigDecimal total = price.multiply(new BigDecimal("1.20")).setScale(2, RoundingMode.HALF_UP);
```

`setScale(2, ...)` returns a new object with two decimal places `[I32]`. `toPlainString()` gives the text without any scientific notation.

### Comparing: `equals` versus `compareTo`

`equals` on a `BigDecimal` requires equal **value and scale**, so `2.0` is **not** equal to `2.00` `[I48]`. `compareTo` compares numerically and says `0` for those two. So:

```java
new BigDecimal("2.0").equals(new BigDecimal("2.00"));       // false
new BigDecimal("2.0").compareTo(new BigDecimal("2.00"));    // 0
```

To ask "do these amounts match?", use `compareTo(...) == 0`. (A `HashSet<BigDecimal>` treats `2.0` and `2.00` as different, too.)

### Which to choose

| | Whole pence (`int`/`long`) | `BigDecimal` |
|---|---|---|
| Good for | simple amounts, adding up, storage, comparisons | percentages, tax, interest, many decimal places, currencies with different minor units |
| Cost | you handle rounding and conversion yourself | more verbose, slower, `equals` surprises |

Either is correct if you are **consistent** and **explicit about rounding**. What isn't acceptable is `double`.

## Worked examples

### Example 1: a total with VAT

*Task: add up prices given as text like `"19.99"`, add 20% VAT, and give the total rounded to 2 places.*

**Step 1 — Prices are text,** so make `BigDecimal`s from the strings.

**Step 2 — Add them up,** starting from `BigDecimal.ZERO`.

**Step 3 — Multiply by `(100 + vat) / 100`,** and finish with `setScale(2, RoundingMode.HALF_UP)`.

```java
String total(List<String> prices, int vatPercent) {
    BigDecimal sum = BigDecimal.ZERO;
    for (String price : prices) {
        sum = sum.add(new BigDecimal(price));
    }
    BigDecimal withVat = sum.multiply(BigDecimal.valueOf(100 + vatPercent)).divide(BigDecimal.valueOf(100));
    return withVat.setScale(2, RoundingMode.HALF_UP).toPlainString();
}
```

**Step 4 — Check.** `["19.99", "5.50"]` at 20% is `30.59` (25.49 × 1.2 = 30.588, rounded half up). The `divide` by 100 is exact here, because dividing by 100 always terminates.

### Example 2: sharing a bill

*Task: split 1000 pence among 3 people so the shares add up to 1000.*

**Step 1 — Base share:** 1000 / 3 = 333. **Leftover:** 1000 % 3 = 1.

**Step 2 — The first `leftover` people pay one more.**

**Step 3 — Result:** `[334, 333, 333]`.

## Where this is used

- **Every financial system** uses whole units or `BigDecimal`. Using `double` is a well-known source of real bugs.
- **Tax, interest and currency conversion** need a stated rounding mode, and auditors check it.
- **Splitting costs fairly** (bills, rent, shipping) needs the leftover rule.

## Common mistakes

:::mistake{id=MC85}
**Using `double` for money.** `0.1 + 0.2` is not `0.3`, and errors accumulate. Use whole pence or `BigDecimal`.
:::

:::mistake{id=MC86}
**Comparing `BigDecimal` with `equals`.** `2.0` and `2.00` aren't equal by `equals` because the scale differs. Use `compareTo(...) == 0`.
:::

:::mistake{id=MC87}
**Dividing without a scale and rounding mode.** If the exact answer has infinitely many digits, `divide` throws an `ArithmeticException`.
:::

## Practice

::exercise{id=j3-l5.2-write-total}

::exercise{id=j3-l5.2-write-split}

::exercise{id=j3-l5.2-debug-double}

::exercise{id=j3-l5.2-explain-money}

## Further reading

- **`java.math.BigDecimal`** `[I32]` `[I48]` documents immutability, scale, `equals` and `compareTo`.
- **`java.math.RoundingMode`** `[I46]` lists the rounding modes.
- **McCauley et al. (2008)** `[R16]` on debugging: an error of one penny only shows up on certain amounts, so test amounts at the rounding boundary.

## How you'll be assessed

- The **write** exercises check that you can calculate with `BigDecimal` and share an amount in whole pence (*implementation*).
- The **debug** exercise checks that you can replace `double` arithmetic with `BigDecimal` (*debugging*).
- The **explain** exercise checks that you can say why `double` is wrong and how to compare `BigDecimal` values (*explanation*).
''' + FOOT)

ex = Exercises("j3-l5.2")
def tot(prices, vat):
    s = sum((Decimal(p) for p in prices), Decimal(0))
    v = (s * (100 + vat) / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return format(v, "f")
TOT_SOL = 'String total(List<String> prices, int vatPercent) {\n    BigDecimal sum = BigDecimal.ZERO;\n    for (String price : prices) {\n        sum = sum.add(new BigDecimal(price));\n    }\n    BigDecimal withVat = sum.multiply(BigDecimal.valueOf(100 + vatPercent)).divide(BigDecimal.valueOf(100));\n    return withVat.setScale(2, RoundingMode.HALF_UP).toPlainString();\n}'
ex.method("write", "j3-l5.2-write-total", "A total with VAT", ["o2"], ["J3.11"], ["IMPL"],
    "Write `total(List<String> prices, int vatPercent)`: add up the prices (text such as `\"19.99\"`) **exactly**, add the VAT percentage, and return the result **rounded to 2 decimal places, halves rounding up**, as plain text, e.g. `30.59`. Use `BigDecimal`.",
    [("total", [("prices", "List<String>"), ("vatPercent", "int")], "String")], {"total": tot},
    [("total", [["19.99", "5.50"], 20]), ("total", [[], 20]), ("total", [["10.00"], 0])],
    [("total", [["0.10", "0.20"], 0]), ("total", [["9.99"], 20]), ("total", [["1.25"], 10]), ("total", [["100.00", "0.01"], 5]), ("total", [["0.05"], 10]), ("total", [["2.50", "2.50", "2.50"], 20])],
    'String total(List<String> prices, int vatPercent) {\n    return "";\n}',
    TOT_SOL,
    {"rounds-down": TOT_SOL.replace("RoundingMode.HALF_UP", "RoundingMode.DOWN"),
     "no-vat": TOT_SOL.replace("BigDecimal.valueOf(100 + vatPercent)", "BigDecimal.valueOf(100)")},
    ("Make BigDecimals from the strings, add them, multiply by (100 + vat) and divide by 100, then setScale(2, RoundingMode.HALF_UP).", "sum.multiply(BigDecimal.valueOf(100 + vatPercent)).divide(BigDecimal.valueOf(100)).setScale(2, RoundingMode.HALF_UP)"),
    source_tests=[("uses BigDecimal", ["BigDecimal"], ["double", "Double"])],
    difficulty=3)
def split(total, people):
    return [total // people + (1 if i < total % people else 0) for i in range(people)]
SPL_SOL = 'List<Integer> split(int totalPence, int people) {\n    List<Integer> shares = new ArrayList<>();\n    for (int i = 0; i < people; i++) {\n        shares.add(totalPence / people + (i < totalPence % people ? 1 : 0));\n    }\n    return shares;\n}'
ex.method("write", "j3-l5.2-write-split", "Share a bill without losing a penny", ["o2"], ["J3.11"], ["IMPL"],
    "Write `split(int totalPence, int people)`: share the total among the people so that the shares **add up exactly to the total**. Everyone pays the same, except that the leftover pennies go one each to the **first** people. `split(1000, 3)` is `[334, 333, 333]`. Return the list of shares in order. (`people` is at least 1.)",
    [("split", [("totalPence", "int"), ("people", "int")], "List<Integer>")], {"split": split},
    [("split", [1000, 3]), ("split", [100, 4]), ("split", [5, 1])],
    [("split", [0, 3]), ("split", [1, 3]), ("split", [2, 5]), ("split", [999, 10]), ("split", [7, 7]), ("split", [10, 3])],
    'List<Integer> split(int totalPence, int people) {\n    List<Integer> shares = new ArrayList<>();\n    for (int i = 0; i < people; i++) {\n        shares.add(totalPence / people);\n    }\n    return shares;\n}',
    SPL_SOL,
    {"leftover-to-last": SPL_SOL.replace("(i < totalPence % people ? 1 : 0)", "(i >= people - totalPence % people ? 1 : 0)"),
     "everyone-pays-extra": SPL_SOL.replace("(i < totalPence % people ? 1 : 0)", "(totalPence % people > 0 ? 1 : 0)")},
    ("Everyone gets total / people. The leftover is total % people pennies; who pays one extra?", "shares.add(totalPence / people + (i < totalPence % people ? 1 : 0));"),
    difficulty=3)
DBL_BAD = 'String addPrices(String a, String b) {\n    double sum = Double.parseDouble(a) + Double.parseDouble(b);\n    return String.valueOf(sum);\n}'
DBL_OK = 'String addPrices(String a, String b) {\n    return new BigDecimal(a).add(new BigDecimal(b)).toPlainString();\n}'
def add_prices(a, b): return format(Decimal(a) + Decimal(b), "f")
ex.method("debug", "j3-l5.2-debug-double", "The penny that wasn't there", ["o1", "o2"], ["J3.11"], ["DEBUG"],
    "`addPrices(\"0.1\", \"0.2\")` should return `0.3`, but returns `0.30000000000000004`. Find the cause and fix `addPrices` so it adds the two prices **exactly** and returns the sum as plain text (keeping the larger number of decimal places: `\"1.50\"` + `\"2.5\"` is `4.00`).",
    [("addPrices", [("a", "String"), ("b", "String")], "String")], {"addPrices": add_prices},
    [("addPrices", ["0.1", "0.2"]), ("addPrices", ["1.50", "2.5"]), ("addPrices", ["10", "5"])],
    [("addPrices", ["0.7", "0.1"]), ("addPrices", ["19.99", "0.01"]), ("addPrices", ["100.10", "200.20"]), ("addPrices", ["0.01", "0.02"]), ("addPrices", ["3.30", "3.30"])],
    DBL_BAD, DBL_OK,
    {"still-double": 'String addPrices(String a, String b) {\n    double sum = Double.parseDouble(a) + Double.parseDouble(b);\n    return String.format("%.2f", sum);\n}'},
    ("What does a double store for 0.1? Which type stores decimals exactly?", "new BigDecimal(a).add(new BigDecimal(b)).toPlainString()"),
    source_tests=[("uses BigDecimal, not double", ["BigDecimal"], ["double", "Double"])],
    difficulty=3)
ex.explain("j3-l5.2-explain-money", "Why not double?", ["o1", "o3"], ["J3.11"],
    "(a) Explain, using `0.1 + 0.2`, why `double` is a bad choice for money. (b) Describe two correct ways to represent money in Java. (c) A test does `new BigDecimal(\"2.0\").equals(new BigDecimal(\"2.00\"))` and gets `false`. Explain why, and what to use to ask whether two amounts are numerically equal.",
    "A full answer says double is binary and can't store 0.1 and 0.2 exactly so 0.1 + 0.2 gives 0.30000000000000004 and errors accumulate; two correct ways are whole pence in an int or long, or BigDecimal built from strings with an explicit scale and rounding mode; and equals on BigDecimal also compares scale so 2.0 and 2.00 differ, so use compareTo(...) == 0.",
    {2: ("Explains that double is binary and gives 0.30000000000000004 with accumulating errors; names whole pence and BigDecimal (from strings, explicit rounding); and says BigDecimal.equals compares scale too, so use compareTo == 0.",
         ["A double stores numbers in binary and can't hold 0.1 or 0.2 exactly, so 0.1 + 0.2 is 0.30000000000000004, and small errors build up. I'd use whole pence in an int or long, or BigDecimal created from strings with an explicit RoundingMode. BigDecimal.equals compares the scale as well as the value, so 2.0 and 2.00 aren't equal; use compareTo and check for 0.",
          "double can't represent 0.1 exactly, so sums are slightly off and == fails. Correct options: whole pence, or BigDecimal with a stated scale and rounding. 2.0 and 2.00 have different scales so equals is false; compareTo(...) == 0 compares the values."]),
     1: ("Covers one or two parts well, for example the double problem but not the equals/compareTo point.",
         ["double isn't exact.", "Use compareTo."]),
     0: ("Incorrect, for example says double is fine if you round at the end, or that BigDecimal.equals compares only the value.",
         ["double is fine for money.", "equals ignores scale."])})
reg({"j3-l5.2": ("Money and BigDecimal", ["J3.11"])},
    {"MC85": (["J3.11"], "Platform", "double is fine for money if you print two decimal places"),
     "MC86": (["J3.11"], "I48", "BigDecimal.equals ignores the scale, so 2.0 equals 2.00"),
     "MC87": (["J3.11"], "Platform", "BigDecimal.divide always works without a scale or rounding mode")})

# ====================================================================== 3.5.3
Lesson("j3-l5.3", "Strings in depth", ["J3.12"], [
    ("o1", "Build text efficiently with StringBuilder, and join lists of items into a sentence"),
    ("o2", "Format aligned output with String.format and formatted"),
    ("o3", "Use a text block for multi-line text, and say how its indentation works"),
], ["j3-l5.2", "j1-l2.4"], 45, ["I47", "I49", "I28", "R8"], r'''
## Before you start

You should know the basic `String` methods ([Working with strings](j1-l2.4)) and that strings are immutable.

**Quick check.** What does `"abc".toUpperCase()` do to the original string?

<details><summary>Show the answer</summary>

Nothing. Strings are immutable; it returns a **new** string.

</details>

## Explanation

### Building text in a loop: `StringBuilder`

Because a `String` can't change, `result += item` in a loop creates a new string every time. For a handful of items that doesn't matter; for thousands it wastes work. A **`StringBuilder`** is a **mutable** sequence of characters `[I47]`: you `append` to it and turn it into a `String` at the end.

```java
StringBuilder sb = new StringBuilder();
for (String name : names) {
    if (!sb.isEmpty()) sb.append(", ");
    sb.append(name);
}
String text = sb.toString();
```

A few more methods: `sb.length()`, `sb.insert(0, "x")`, `sb.reverse()`, `sb.setLength(0)` to empty it. For simple "join with a separator", `String.join(", ", names)` (or `Collectors.joining`) is even shorter `[I49]`.

A tricky bit of real text: **a list as a sentence**: `[]` → `nothing`, `[a]` → `a`, `[a, b]` → `a and b`, `[a, b, c]` → `a, b and c`. The last item is joined with "and", all the earlier ones with commas. That's a loop with a special case at the end, a good use of an index loop and a `StringBuilder`.

### Formatting: `String.format` and `formatted`

`String.format(pattern, args...)` fills format codes in a pattern `[I49]`. `"...".formatted(args...)` does the same, written on the string itself:

```java
String.format("%s has %d items", "Ada", 3);       // "Ada has 3 items"
"%s has %d items".formatted("Ada", 3);            // the same
```

The format codes you'll use most:

| Code | Meaning | Example |
|---|---|---|
| `%s` | any value as text | `%s` |
| `%d` | a whole number | `%d` |
| `%.2f` | a decimal number with 2 decimal places | `%.2f` |
| `%5d` | right-aligned in a field 5 wide | `%5d` |
| `%-10s` | left-aligned in a field 10 wide | `%-10s` |
| `%05d` | zero-padded to width 5 | `%05d` |
| `%%` | a literal percent sign | `%%` |

Widths make aligned columns:

```java
String line = "%-10s%8s".formatted("Tea", "£1.50");     // "Tea         £1.50"
```

A formatting pattern is a small language of its own; keep to the few above. (Don't format money with `%.2f` and a `double`: build the pounds-and-pence text from whole pence, as you did in Stage 1.)

### Text blocks: multi-line strings

Multi-line text is awkward with `"\n"` everywhere. A **text block** starts with `"""` followed by a newline, and ends with `"""` `[I28]`:

```java
String letter = """
        Dear Ada,

        Your order has shipped.
        """;
```

How it works:

- The text starts on the line **after** the opening `"""`.
- Java removes the **common leading spaces** shared by all lines (the *incidental indentation*), so you can indent the text to line up with your code without that indentation ending up in the string. The position of the closing `"""` counts too: if it's on its own line indented as far as the text, the text keeps no leading spaces, and the string **ends with a newline**.
- You rarely need `\n` or `\"` inside a text block.

Combine it with `formatted` for templates:

```java
String letter(String name) {
    return """
            Dear %s,

            Your order has shipped.
            """.formatted(name);
}
```

That returns `"Dear Ada,\n\nYour order has shipped.\n"` for `"Ada"`. Text blocks are good for SQL, JSON and email templates.

### Other useful methods

| Method | What it does |
|---|---|
| `strip()` | removes spaces from both ends (preferred over `trim()`) |
| `isBlank()` | true if empty or only spaces |
| `repeat(n)` | the string repeated `n` times |
| `lines()` | a stream of the lines |
| `String.join(sep, items)` | joins with a separator |

## Worked examples

### Example 1: a list as a sentence

*Task: `[a, b, c]` → `a, b and c`.*

**Step 1 — Cases:** none, one, two, many.

**Step 2 — For each item, decide what goes before it:** nothing for the first; `" and "` for the last (when it isn't also the first); `", "` otherwise.

```java
String sentence(List<String> items) {
    if (items.isEmpty()) {
        return "nothing";
    }
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < items.size(); i++) {
        if (i > 0) {
            sb.append(i == items.size() - 1 ? " and " : ", ");
        }
        sb.append(items.get(i));
    }
    return sb.toString();
}
```

**Step 3 — Check.** `[a, b]` → `a and b`; `[a, b, c]` → `a, b and c`.

### Example 2: aligned columns

*Task: print a name left-aligned in 10 characters and an amount right-aligned in 8.*

**Step 1 — Use widths:** `"%-10s%8s"`.

**Step 2 — Build each line, and join with newlines:**

```java
String row = "%-10s%8s".formatted("Tea", "£1.50");
```

## Where this is used

- **Reports, receipts and logs** need aligned columns and clean sentences.
- **Templates** for emails and messages are text blocks with `formatted`.
- **Performance:** building big strings in loops with `+=` is a classic slowdown.

## Common mistakes

:::mistake{id=MC88}
**Building a large string with `+=` in a loop.** Each `+=` makes a new string. Use `StringBuilder` or `String.join`.
:::

:::mistake{id=MC89}
**Expecting a text block to keep the indentation of your code.** Java strips the common leading spaces. The closing `"""` position affects how much is stripped, and whether there is a trailing newline.
:::

## Practice

::exercise{id=j3-l5.3-write-sentence}

::exercise{id=j3-l5.3-write-table}

::exercise{id=j3-l5.3-modify-textblock}

## Version notes

**Text blocks** were added in **Java 15** `[I28]`, and `String.formatted` in **Java 15**. Before that, multi-line text meant `"\n"` and `+` everywhere.

## Further reading

- **`java.lang.StringBuilder` and `ArrayList`** `[I47]`.
- **`java.lang.String`** `[I49]` for `format`, `formatted`, `strip`, `repeat` and `join`.
- **JEP 378: Text Blocks** `[I28]` explains the indentation rules in detail.
- **Qian & Lehman (2017)** `[R8]`.

## How you'll be assessed

- The **write** exercises check that you can build a sentence with `StringBuilder` and align columns with a format (*implementation*).
- The **modify** exercise checks that you can convert concatenation into a text block with `formatted` (*modification*).
''' + FOOT, features=[("text blocks", 15), ("String.formatted", 15)])

ex = Exercises("j3-l5.3")
def sentence(items):
    if not items: return "nothing"
    if len(items) == 1: return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]
SEN_SOL = 'String sentence(List<String> items) {\n    if (items.isEmpty()) {\n        return "nothing";\n    }\n    StringBuilder sb = new StringBuilder();\n    for (int i = 0; i < items.size(); i++) {\n        if (i > 0) {\n            sb.append(i == items.size() - 1 ? " and " : ", ");\n        }\n        sb.append(items.get(i));\n    }\n    return sb.toString();\n}'
ex.method("write", "j3-l5.3-write-sentence", "A list as a sentence", ["o1"], ["J3.12"], ["IMPL"],
    "Write `sentence(List<String> items)` using a `StringBuilder`: an empty list is `nothing`; one item is just that item; two items are `a and b`; more are `a, b and c` (commas between all but the last two, and `and` before the last).",
    [("sentence", [("items", "List<String>")], "String")], {"sentence": sentence},
    [("sentence", [["a", "b", "c"]]), ("sentence", [[]]), ("sentence", [["x"]])],
    [("sentence", [["tea", "coffee"]]), ("sentence", [["a", "b", "c", "d"]]), ("sentence", [["only one"]]), ("sentence", [["red", "green", "blue"]]), ("sentence", [["1", "2", "3", "4", "5"]])],
    'String sentence(List<String> items) {\n    return "";\n}',
    SEN_SOL,
    {"no-and": SEN_SOL.replace('i == items.size() - 1 ? " and " : ", "', '", "'),
     "oxford-comma": SEN_SOL.replace('i == items.size() - 1 ? " and " : ", "', 'i == items.size() - 1 && items.size() > 2 ? ", and " : (i == items.size() - 1 ? " and " : ", ")')},
    ("Handle the empty list first. In the loop, decide what to add before each item except the first: \" and \" before the last, otherwise \", \".", "sb.append(i == items.size() - 1 ? \" and \" : \", \");"),
    source_tests=[("uses a StringBuilder", ["StringBuilder"], None)],
    difficulty=3)
def money(p): return f"£{p // 100}.{p % 100:02d}"
def table(names, pence):
    return "\n".join(f"{n:<10}{money(p):>8}" for n, p in zip(names, pence))
TAB_SOL = 'String table(String[] names, int[] pence) {\n    StringBuilder sb = new StringBuilder();\n    for (int i = 0; i < names.length; i++) {\n        if (i > 0) {\n            sb.append("\\n");\n        }\n        String money = "£" + pence[i] / 100 + "." + String.format("%02d", pence[i] % 100);\n        sb.append(String.format("%-10s%8s", names[i], money));\n    }\n    return sb.toString();\n}'
ex.method("write", "j3-l5.3-write-table", "Aligned columns", ["o2"], ["J3.12"], ["IMPL"],
    "Write `table(String[] names, int[] pence)`: one line per item, with the **name left-aligned in 10 characters** and the price (as `£1.99`, built from whole pence) **right-aligned in 8 characters**, lines joined by `\\n` (none after the last). For `\"Tea\"` and `150` the line is `Tea         £1.50`. Use `String.format` or `formatted`.",
    [("table", [("names", "String[]"), ("pence", "int[]")], "String")], {"table": table},
    [("table", [["Tea", "Cake"], [150, 275]]), ("table", [[], []]), ("table", [["Milk"], [99]])],
    [("table", [["a"], [5]]), ("table", [["Sandwich", "Soup"], [1000, 0]]), ("table", [["Pie"], [12345]]), ("table", [["X", "Y", "Z"], [1, 10, 100]]), ("table", [["Longername"], [5]])],
    'String table(String[] names, int[] pence) {\n    return "";\n}',
    TAB_SOL,
    {"right-aligned-name": TAB_SOL.replace("%-10s%8s", "%10s%8s"),
     "wrong-width": TAB_SOL.replace("%-10s%8s", "%-10s%9s")},
    ("%-10s pads a name on the right to 10 wide; %8s pads the price on the left to 8 wide. Build the pounds-and-pence text from whole pence.", "String.format(\"%-10s%8s\", names[i], money)"),
    source_tests=[("uses a format", ["format"], None)],
    difficulty=3)
TB_BAD = 'String letter(String name) {\n    return "Dear " + name + ",\\n\\nYour order has shipped.\\n";\n}'
TB_OK = 'String letter(String name) {\n    return """\n            Dear %s,\n\n            Your order has shipped.\n            """.formatted(name);\n}'
ex.method("modify", "j3-l5.3-modify-textblock", "Concatenation to a text block", ["o3"], ["J3.12"], ["MOD"],
    "`letter` builds a three-line message with `+` and `\\n`. Rewrite it with a **text block** and `formatted`, so the text is easy to read, and returns exactly the same string: `Dear <name>,`, a blank line, `Your order has shipped.`, and a final newline.",
    [("letter", [("name", "String")], "String")], {"letter": lambda n: f"Dear {n},\n\nYour order has shipped.\n"},
    [("letter", ["Ada"]), ("letter", [""]), ("letter", ["Bo Lee"])],
    [("letter", ["Grace"]), ("letter", ["O'Brien"]), ("letter", ["100%"]), ("letter", ["x"]), ("letter", ["Zed Z"])],
    TB_BAD, TB_OK,
    {"no-trailing-newline": TB_OK.replace("shipped.\n            \"\"\"", "shipped.\"\"\"").replace("\"\"\"\n            Dear", "\"\"\"\n            Dear")},
    ("Start the text on the line after the opening \"\"\", put %s where the name goes, and end with .formatted(name). Put the closing \"\"\" on its own line for the final newline.", "return \"\"\"\\n    Dear %s,\\n\\n    Your order has shipped.\\n    \"\"\".formatted(name);"),
    source_tests=[("uses a text block", ['"""', ".formatted("], ['\\n'])],
    difficulty=3)
reg({"j3-l5.3": ("Strings in depth", ["J3.12"])},
    {"MC88": (["J3.12"], "Platform", "Building a large string with += in a loop is efficient"),
     "MC89": (["J3.12"], "I28", "A text block keeps all the indentation of the source code")})
print("3.4 and 3.5 written")
