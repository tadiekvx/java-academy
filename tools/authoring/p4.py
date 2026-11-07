from proj import *

def avg(m): return 0.0 if not m else sum(m) / len(m)
def grade(x): return "A" if x >= 70 else "B" if x >= 60 else "C" if x >= 50 else "Fail"
def passing(m, p): return sum(1 for x in m if x >= p)
def highest(m): return max(m) if m else -1
def summary(m, p):
    if not m: return "No students"
    n, k = len(m), passing(m, p)
    return f"{n} students, {k} passed ({k * 100 // n}%), highest {max(m)}"

SOLUTION = '''
double average(int[] marks) {
    if (marks.length == 0) {
        return 0.0;
    }
    int total = 0;
    for (int i = 0; i < marks.length; i++) {
        total += marks[i];
    }
    return (double) total / marks.length;
}

String grade(int mark) {
    if (mark >= 70) {
        return "A";
    } else if (mark >= 60) {
        return "B";
    } else if (mark >= 50) {
        return "C";
    } else {
        return "Fail";
    }
}

int countPassing(int[] marks, int passMark) {
    int count = 0;
    for (int i = 0; i < marks.length; i++) {
        if (marks[i] >= passMark) {
            count++;
        }
    }
    return count;
}

int highest(int[] marks) {
    if (marks.length == 0) {
        return -1;
    }
    int best = marks[0];
    for (int mark : marks) {
        if (mark > best) {
            best = mark;
        }
    }
    return best;
}

String summary(int[] marks, int passMark) {
    if (marks.length == 0) {
        return "No students";
    }
    int passed = countPassing(marks, passMark);
    return marks.length + " students, " + passed + " passed (" + passed * 100 / marks.length + "%), highest " + highest(marks);
}

void main() {
    int[] marks = {72, 58, 91, 40};
    IO.println(summary(marks, 50));
}
'''
STARTER = '''
// Inherited code: the class gradebook of a teacher who has left.
// It compiles and mostly looks plausible, but three bug reports have come in (see the milestones),
// and two things have to be added. Nobody remembers who wrote it, and there are no tests.

double average(int[] marks) {
    int total = 0;
    for (int i = 0; i < marks.length; i++) {
        total += marks[i];
    }
    return total / marks.length;
}

String grade(int mark) {
    if (mark >= 50) {
        return "C";
    } else if (mark >= 60) {
        return "B";
    } else if (mark >= 70) {
        return "A";
    } else {
        return "Fail";
    }
}

int countPassing(int[] marks, int passMark) {
    int count = 0;
    for (int i = 0; i < marks.length - 1; i++) {
        if (marks[i] > passMark) {
            count++;
        }
    }
    return count;
}

void main() {
    int[] marks = {72, 58, 91, 40};
    IO.println(average(marks));
    IO.println(grade(marks[0]));
    IO.println(countPassing(marks, 50));
}
'''
S = SOLUTION
wrongs = {
  "m1-only-the-empty-case": S.replace("return (double) total / marks.length;", "return total / marks.length;"),
  "m1-no-empty-guard": S.replace("    if (marks.length == 0) {\n        return 0.0;\n    }\n    int total = 0;", "    int total = 0;"),
  "m2-reordered-but-strict": S.replace("mark >= 70", "mark > 70").replace("mark >= 60", "mark > 60"),
  "m3-still-skips-last": S.replace("for (int i = 0; i < marks.length; i++) {\n        if (marks[i] >= passMark) {", "for (int i = 0; i < marks.length - 1; i++) {\n        if (marks[i] >= passMark) {"),
  "m3-still-strict": S.replace("marks[i] >= passMark", "marks[i] > passMark"),
  "m4-lowest": S.replace("if (mark > best) {", "if (mark < best) {"),
  "m5-percent-of-passes": S.replace("passed * 100 / marks.length", "passed * 100 / (marks.length - passed + 1)"),
}
def c(m, p=None): return [m] if p is None else [m, p]
ms = [
 dict(id="m1", title="Bug report 1: the wrong averages", methods=[("average", [("marks", "int[]")], "double")], fns={"average": avg},
  instructions="""
  **Bug report:** *"The average for {70, 80, 90, 91} shows 82.0 but should be 82.75. And the program crashed when I tried an empty class."*

  Find the causes in the inherited `average` and fix them. An empty class has an average of `0.0`.
  """,
  visible=[(None, [[70, 80, 90, 91]]), (None, [[]]), (None, [[50, 51]])],
  hidden=[(None, [[1]], "one mark"), (None, [[0, 0, 0]], "all zero"), (None, [[99, 100]], "high marks"), (None, [[33, 33, 34]], "thirds"), (None, [[100, 0]], "extremes")]),
 dict(id="m2", title="Bug report 2: nobody gets an A", methods=[("grade", [("mark", "int")], "String")], fns={"grade": grade},
  instructions="""
  **Bug report:** *"A student with 85 was given a C."*

  The rules are: 70 or more is `"A"`, 60 or more is `"B"`, 50 or more is `"C"`, anything lower is `"Fail"`. Find the cause in `grade` and fix it.
  """,
  visible=[(None, [85]), (None, [65]), (None, [20])],
  hidden=[(None, [70], "exactly 70"), (None, [69], "just under 70"), (None, [60], "exactly 60"), (None, [59], "just under 60"), (None, [50], "exactly 50"), (None, [49], "just failing"), (None, [100], "full marks"), (None, [0], "zero")]),
 dict(id="m3", title="Bug report 3: the pass count is off", methods=[("countPassing", [("marks", "int[]"), ("passMark", "int")], "int")], fns={"countPassing": passing},
  instructions="""
  **Bug report:** *"With a pass mark of 50, the class {50, 60, 40, 70} shows 1 pass. It should be 3: a student on exactly the pass mark passes. And a pass by the last student in the list is never counted."*

  There are two separate faults in `countPassing`. Find both, fixing one at a time and checking after each.
  """,
  visible=[(None, [[50, 60, 40, 70], 50]), (None, [[], 50]), (None, [[10, 20, 80], 50])],
  hidden=[(None, [[50], 50], "single student on the mark"), (None, [[49, 50, 51], 50], "either side"), (None, [[100, 100], 100], "all on a high mark"), (None, [[0, 0], 0], "pass mark zero"), (None, [[40, 41, 42, 43], 43], "only the last passes")]),
 dict(id="m4", title="New feature: the top mark", methods=[("highest", [("marks", "int[]")], "int")], fns={"highest": highest},
  instructions="""
  **Feature request:** *"Please add `highest`, which returns the highest mark in the class, or -1 if there are no marks."*

  The inherited program doesn't have it. Add `int highest(int[] marks)`.
  """,
  visible=[(None, [[72, 58, 91, 40]]), (None, [[]]), (None, [[5]])],
  hidden=[(None, [[0, 0]], "all zero"), (None, [[91, 72]], "first is highest"), (None, [[1, 2, 3, 4, 5]], "last is highest"), (None, [[50, 50]], "tie"), (None, [[100, 99, 100]], "repeated top")]),
 dict(id="m5", title="Change request: the class summary", methods=[("summary", [("marks", "int[]"), ("passMark", "int")], "String")], fns={"summary": summary},
  instructions="""
  **Change request:** *"The head teacher wants a one-line summary of each class."*

  Add `String summary(int[] marks, int passMark)` returning `N students, K passed (P%), highest H`, where K is the number who passed, P is K as a whole-number percentage of N (rounded **down**), and H is the highest mark. For example, `{72, 58, 91, 40}` with a pass mark of 50 gives `4 students, 3 passed (75%), highest 91`. An empty class gives `No students`.

  Reuse the methods you've already fixed and added.
  """,
  visible=[(None, [[72, 58, 91, 40], 50]), (None, [[], 50]), (None, [[50], 50])],
  hidden=[(None, [[10, 20, 30], 50], "nobody passes"), (None, [[60, 70, 80], 50], "everybody passes"), (None, [[50, 49, 51], 50], "two thirds"), (None, [[100], 101], "just below the mark"), (None, [[70, 30, 31, 32, 33, 34, 35], 33], "awkward percentage")]),
]
rubric = [
 ("Diagnosis", "Changed code at random until tests passed, or fixed only the symptom", "Found the causes for most reports, but could not explain one", "Reproduced each report, named its cause, and fixed that cause only"),
 ("Safe change", "Fixes broke earlier behaviour", "No regressions, but changed more than necessary", "Smallest change per fault; earlier milestones still pass"),
 ("Reuse", "New methods repeat logic that already existed", "Some reuse", "summary builds on countPassing and highest"),
 ("Explanation", "Missing, or only says what the code does", "Names the faults but not how they were found", "States each fault, how it was found, and what a test for it would look like"),
]
project("j1-a1-inherited-gradebook", "Stage 1 assessment: the inherited gradebook", "C",
    "Independent assessment: fix bugs you didn't write, add a feature, and absorb a change request.",
    """
    This is the **Stage 1 independent assessment**. There are no lessons for it and no step-by-step instructions. You've been given a working-looking program that someone else wrote, **three bug reports**, a **new feature** and a **change request**. That's what the first week of a real job looks like.

    The AI mentor isn't available inside projects, so this shows what you can do on your own. If part of it is hard, that's useful information: it tells you what to revisit.

    Work like a professional: **reproduce** each report, form a hypothesis, change **one thing at a time**, and check your earlier milestones still pass. A bug can have more than one cause.

    Money isn't involved. Marks are whole numbers from 0 to 100.
    """, 3, ["j1-l6.5", "j1-l5.5"], ["J1.07", "J1.08", "J1.10", "J1.13", "J1.14"],
    ["Fix the three reported bugs without changing what already works.",
     "Add `highest` and `summary` as described, reusing existing methods.",
     "Marks are whole numbers from 0 to 100; a class may be empty."],
    ["Do not rewrite the program from scratch: change as little as possible.", "Fix one fault at a time and re-check."],
    ["Given {70, 80, 90, 91}, then average is 82.75.",
     "Given 70 marks of 85, then grade is A.",
     "Given a pass mark of 50 and a student on exactly 50, then they are counted as passing.",
     "Given an empty class, then average is 0.0, highest is -1 and summary is No students."],
    ms, rubric,
    "In 150 words or fewer: For each bug report, say what the fault was and how you found it. Then say what test you would have added to stop it coming back.",
    STARTER, SOLUTION, wrongs)
print("assessment written")
