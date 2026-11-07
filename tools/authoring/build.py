"""Authoring helper for Stage 1 content (session tool, not part of the repo).

Writes lesson Markdown and exercise directories in the format of
docs/curriculum/03-content-standards.md. Expected values for method tests are computed by an
independent Python implementation, so the validator's run of the Java reference solution
cross-checks both.
"""
import json
import math
import os
import textwrap

ROOT = "/Users/brandon/Documents/Java/content/java/stage-1"


def q(value):
    """A YAML-safe scalar (JSON is valid YAML)."""
    return json.dumps(value, ensure_ascii=False)


def block(text, indent=2):
    return textwrap.indent(textwrap.dedent(text).strip("\n"), " " * indent)


def code(text):
    return textwrap.dedent(text).strip("\n") + "\n"


def jdiv(a, b):
    """Java int division: truncates toward zero."""
    return int(a / b) if (a < 0) != (b < 0) and a % b != 0 else a // b


def jmod(a, b):
    return a - b * jdiv(a, b)


class Lesson:
    def __init__(self, id, title, concepts, objectives, prereqs, minutes, sources, body, features=(), resources=()):
        self.id = id
        if not resources:
            try:
                resources = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lesson_resources.json"))).get(id, ())
            except OSError:
                resources = ()
        front = [
            "---",
            f"id: {id}",
            f"title: {q(title)}",
            f"concepts: [{', '.join(concepts)}]",
            "objectives:",
        ]
        front += [f"  - {{id: {oid}, text: {q(text)}}}" for oid, text in objectives]
        front += [
            f"prerequisites: [{', '.join(prereqs)}]",
            f"estimated_minutes: {minutes}",
            "status: in_review",
            "authors: [Claude (AI draft)]",
            "ai_assisted: true",
            "technical_review: {by: null, date: null}",
            "pedagogy_review: {by: null, date: null}",
            f"sources: [{', '.join(sources)}]",
            "features: [" + ", ".join(f"{{name: {q(n)}, since: {v}}}" for n, v in features) + "]",
        ] + ([f"resources: [{', '.join(resources)}]"] if resources else []) + [
            "---",
            "",
        ]
        os.makedirs(f"{ROOT}/lessons", exist_ok=True)
        with open(f"{ROOT}/lessons/{id}.md", "w") as f:
            f.write("\n".join(front) + textwrap.dedent(body).strip("\n") + "\n")


class Exercises:
    def __init__(self, lesson):
        self.lesson = lesson

    def _dir(self, id):
        d = f"{ROOT}/exercises/{id}"
        os.makedirs(d, exist_ok=True)
        return d

    def _head(self, id, type, title, assesses, concepts, evidence, misconceptions, difficulty, role, group, prompt):
        lines = [
            f"id: {id}",
            f"type: {type}",
            f"title: {q(title)}",
            f"lesson: {self.lesson}",
            f"role: {role}",
            f"assesses: [{', '.join(assesses)}]",
            f"concepts: [{', '.join(concepts)}]",
            f"evidence: [{', '.join(evidence)}]",
            f"misconceptions: [{', '.join(misconceptions)}]",
            f"difficulty: {difficulty}",
        ]
        if group:
            lines.append(f"variant_group: {group}")
        lines += ["prompt: |", block(prompt)]
        return lines

    @staticmethod
    def _tail(hints, extra=()):
        return list(extra) + ["hints:", f"  h1: {q(hints[0])}", f"  h2: {q(hints[1])}", "ai_assisted: true", ""]

    def predict(self, id, title, assesses, concepts, prompt, program, expected, hints,
                misconceptions=(), difficulty=1, evidence=("MIST",)):
        d = self._dir(id)
        os.makedirs(f"{d}/starter", exist_ok=True)
        lines = self._head(id, "predict", title, assesses, concepts, evidence, misconceptions, difficulty, "ladder", None, prompt)
        lines += ["expected_output: |", block(expected)]
        lines += self._tail(hints)
        open(f"{d}/exercise.yaml", "w").write("\n".join(lines))
        open(f"{d}/starter/Main.java", "w").write(code(program))

    def parsons(self, id, title, assesses, concepts, prompt, blocks, distractors, stdout, hints,
                misconceptions=(), difficulty=1, stdin=""):
        d = self._dir(id)
        lines = self._head(id, "parsons", title, assesses, concepts, ["IMPL"], misconceptions, difficulty, "ladder", None, prompt)
        lines += ["blocks:"] + [f"  - {q(b)}" for b in blocks]
        lines += ["distractors:"] + [f"  - {q(b)}" for b in distractors]
        lines += ["tests:", "  visible:", f"    - {{name: runs correctly, stdin: {q(stdin)}, stdout_equals: {q(stdout)}}}"]
        lines += self._tail(hints)
        open(f"{d}/exercise.yaml", "w").write("\n".join(lines))

    def method(self, type, id, title, assesses, concepts, evidence, prompt, methods, fns, visible, hidden,
               starter, solution, wrongs, hints, misconceptions=(), difficulty=2, role="ladder", group=None,
               starter_compiles=True, tolerance=None, notes=None, source_tests=()):
        """methods: [(name, [(param, type)], returns)]; fns: {name: python callable};
        visible/hidden: [(method or None, args)] or [(method or None, args, test name)]."""
        d = self._dir(id)
        for sub in ("starter", "solution", "wrong"):
            os.makedirs(f"{d}/{sub}", exist_ok=True)
        lines = self._head(id, type, title, assesses, concepts, evidence, misconceptions, difficulty, role, group, prompt)
        lines += ["entry:", "  methods:"]
        for name, params, returns in methods:
            ps = ", ".join(f"{{name: {p}, type: {q(t)}}}" for p, t in params)
            lines.append(f"    - {{name: {name}, params: [{ps}], returns: {q(returns)}}}")
        default = methods[0][0]

        def case(c):
            method, args = c[0], c[1]
            name = c[2] if len(c) > 2 else None
            m = method or default
            expect = fns[m](*args)
            parts = []
            if name:
                parts.append(f"name: {q(name)}")
            if method:
                parts.append(f"method: {method}")
            parts.append(f"args: {q(args)}")
            parts.append(f"expect: {q(expect)}")
            return "    - {" + ", ".join(parts) + "}"

        lines += ["tests:", "  visible:"] + [case(c) for c in visible]
        for sname, yes, no in source_tests:
            parts = [f"name: {q(sname)}"]
            if yes:
                parts.append(f"source_contains: {q(yes)}")
            if no:
                parts.append(f"source_not_contains: {q(no)}")
            lines.append("    - {" + ", ".join(parts) + "}")
        if hidden:
            lines += ["  hidden:"] + [case(c) for c in hidden]
        if tolerance:
            lines.append(f"  tolerance: {tolerance}")
        extra = [] if starter_compiles else ["starter_compiles: false"]
        lines += self._tail(hints, extra)
        open(f"{d}/exercise.yaml", "w").write("\n".join(lines))
        def with_main(s):
            return s if "void main" in s else s.rstrip() + "\n\nvoid main() {\n}"
        open(f"{d}/starter/Main.java", "w").write(code(with_main(starter)))
        open(f"{d}/solution/Main.java", "w").write(code(with_main(solution)))
        for name, text in wrongs.items():
            open(f"{d}/wrong/{name}.java", "w").write(code(with_main(text)))
        if notes:
            open(f"{d}/reviewer-notes.md", "w").write(code(notes))

    def io(self, type, id, title, assesses, concepts, evidence, prompt, program_fn, visible, hidden,
           starter, solution, wrongs, hints, misconceptions=(), difficulty=2, role="ladder", group=None,
           starter_compiles=True, contains=False, notes=None, source_tests=()):
        """visible/hidden: [(name, stdin)]; program_fn(stdin) -> expected stdout (exact) or list of fragments.
        source_tests: [(name, must_contain, must_not_contain)] structure checks on the learner's source."""
        d = self._dir(id)
        for sub in ("starter", "solution", "wrong"):
            os.makedirs(f"{d}/{sub}", exist_ok=True)
        lines = self._head(id, type, title, assesses, concepts, evidence, misconceptions, difficulty, role, group, prompt)

        def case(c):
            name, stdin = c
            out = program_fn(stdin)
            if contains:
                return f"    - {{name: {q(name)}, stdin: {q(stdin)}, stdout_contains: {q(out)}}}"
            return f"    - {{name: {q(name)}, stdin: {q(stdin)}, stdout_equals: {q(out)}}}"

        lines += ["tests:", "  visible:"] + [case(c) for c in visible]
        for name, yes, no in source_tests:
            parts = [f"name: {q(name)}"]
            if yes:
                parts.append(f"source_contains: {q(yes)}")
            if no:
                parts.append(f"source_not_contains: {q(no)}")
            lines.append("    - {" + ", ".join(parts) + "}")
        if hidden:
            lines += ["  hidden:"] + [case(c) for c in hidden]
        extra = [] if starter_compiles else ["starter_compiles: false"]
        lines += self._tail(hints, extra)
        open(f"{d}/exercise.yaml", "w").write("\n".join(lines))
        open(f"{d}/starter/Main.java", "w").write(code(starter))
        open(f"{d}/solution/Main.java", "w").write(code(solution))
        for name, text in wrongs.items():
            open(f"{d}/wrong/{name}.java", "w").write(code(text))
        if notes:
            open(f"{d}/reviewer-notes.md", "w").write(code(notes))

    def explain(self, id, title, assesses, concepts, prompt, criteria, levels, misconceptions=(), difficulty=2,
                refers_to=None):
        """levels: {2: (descriptor, [samples]), 1: (...), 0: (...)}"""
        d = self._dir(id)
        lines = self._head(id, "explain", title, assesses, concepts, ["EXPL"], misconceptions, difficulty, "ladder", None, prompt)
        if refers_to:
            lines.append(f"refers_to: {refers_to}")
        lines += ["rubric:", "  criteria: |", block(criteria, 4), "  levels:"]
        for score in (2, 1, 0):
            descriptor, samples = levels[score]
            lines += [f"    - score: {score}", f"      descriptor: {q(descriptor)}", "      samples:"]
            lines += [f"        - {q(s)}" for s in samples]
        lines += ["ai_assisted: true", ""]
        open(f"{d}/exercise.yaml", "w").write("\n".join(lines))
