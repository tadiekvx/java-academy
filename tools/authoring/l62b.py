from build import *
ex = Exercises("j1-l6.2")
def totals(v): return [sum(v), sum(v) + 10 * len(v)]
ex.method("debug", "j1-l6.2-debug-alias", "The backup that wasn't", ["o2", "o3"], ["J1.10"], ["DEBUG"],
    "`bonusTotals` gives every score a 10-point bonus in a separate `boosted` array, then returns two numbers in an array: the total of the **original** scores, and the total with the bonus. For `{1, 2, 3}` it should return `{6, 36}`, but it returns `{36, 36}`: the original total has changed too. Find and fix the bug.",
    [("bonusTotals", [("scores", "int[]")], "int[]")], {"bonusTotals": totals},
    [(None, [[1, 2, 3]]), (None, [[]]), (None, [[10]])],
    [(None, [[50, 60]], "two scores"), (None, [[-10, 0, 10]], "negatives"), (None, [[100]], "one score"), (None, [[5, 5, 5, 5]], "four"), (None, [[1, 2, 3, 4, 5, 6]], "six")],
    'int[] bonusTotals(int[] scores) {\n    int[] boosted = scores;\n    for (int i = 0; i < boosted.length; i++) {\n        boosted[i] = boosted[i] + 10;\n    }\n    int before = 0;\n    for (int score : scores) {\n        before += score;\n    }\n    int after = 0;\n    for (int score : boosted) {\n        after += score;\n    }\n    return new int[] {before, after};\n}\n\nvoid main() {\n    IO.println(Arrays.toString(bonusTotals(new int[] {1, 2, 3}))); // should print [6, 36]\n}\n',
    'int[] bonusTotals(int[] scores) {\n    int[] boosted = Arrays.copyOf(scores, scores.length);\n    for (int i = 0; i < boosted.length; i++) {\n        boosted[i] = boosted[i] + 10;\n    }\n    int before = 0;\n    for (int score : scores) {\n        before += score;\n    }\n    int after = 0;\n    for (int score : boosted) {\n        after += score;\n    }\n    return new int[] {before, after};\n}\n\nvoid main() {\n    IO.println(Arrays.toString(bonusTotals(new int[] {1, 2, 3}))); // should print [6, 36]\n}\n',
    {"same-total": 'int[] bonusTotals(int[] scores) {\n    int before = 0;\n    for (int score : scores) {\n        before += score;\n    }\n    return new int[] {before, before};\n}\n\nvoid main() {\n}\n'},
    ("Trace boosted = scores. How many arrays exist after that line?", "boosted and scores are two names for one array. Make boosted a separate copy with Arrays.copyOf(scores, scores.length)."),
    misconceptions=["MC12"])
print("ok")
