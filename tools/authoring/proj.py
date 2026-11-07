import os, textwrap, json
from build import q, block, code, jdiv, jmod, ROOT

def _case(c, fns, default):
    method, args = c[0], c[1]
    name = c[2] if len(c) > 2 else None
    m = method or default
    expect = fns[m](*args)
    parts = []
    if name: parts.append(f"name: {q(name)}")
    if method: parts.append(f"method: {method}")
    parts.append(f"args: {q(args)}")
    parts.append(f"expect: {q(expect)}")
    return "          - {" + ", ".join(parts) + "}"

def project(id, title, category, summary, brief, hours, prereqs, concepts, requirements, constraints, acceptance,
            milestones, rubric, design_prompt, starter, solution, wrongs):
    d = f"{ROOT}/projects/{id}"
    for sub in ("starter", "solution", "wrong"):
        os.makedirs(f"{d}/{sub}", exist_ok=True)
    L = [f"id: {id}", f"title: {q(title)}", f"category: {category}", "status: in_review", f"summary: {q(summary)}",
         "brief: |", block(brief, 2), f"estimated_hours: {hours}", f"prerequisites: [{', '.join(prereqs)}]",
         f"concepts: [{', '.join(concepts)}]"]
    for key, items in (("requirements", requirements), ("constraints", constraints), ("acceptance", acceptance)):
        if items:
            L.append(f"{key}:")
            L += [f"  - {q(i)}" for i in items]
    L.append("milestones:")
    for m in milestones:
        L += [f"  - id: {m['id']}", f"    title: {q(m['title'])}", "    instructions: |", block(m['instructions'], 6)]
        if m.get('methods'):
            L.append("    entry:")
            L.append("      methods:")
            for name, params, returns in m['methods']:
                ps = ", ".join(f"{{name: {p}, type: {q(t)}}}" for p, t in params)
                L.append(f"        - {{name: {name}, params: [{ps}], returns: {q(returns)}}}")
        L.append("    tests:")
        L.append("      visible:")
        if m.get('io'):
            for name, stdin, frags in m['io']['visible']:
                L.append(f"        - {{name: {q(name)}, stdin: {q(stdin)}, stdout_contains: {q(frags)}}}")
            L.append("      hidden:")
            for name, stdin, frags in m['io']['hidden']:
                L.append(f"        - {{name: {q(name)}, stdin: {q(stdin)}, stdout_contains: {q(frags)}}}")
        else:
            default = m['methods'][0][0]
            L += [_case(c, m['fns'], default).replace("          -", "        -", 1) for c in m['visible']]
            for sname, yes, no in m.get('source_tests', ()):
                parts = [f"name: {q(sname)}"]
                if yes: parts.append(f"source_contains: {q(yes)}")
                if no: parts.append(f"source_not_contains: {q(no)}")
                L.append("        - {" + ", ".join(parts) + "}")
            L.append("      hidden:")
            L += [_case(c, m['fns'], default).replace("          -", "        -", 1) for c in m['hidden']]
    if rubric:
        L.append("rubric:")
        for crit, zero, one, two in rubric:
            L += [f"  - criterion: {q(crit)}", f"    zero: {q(zero)}", f"    one: {q(one)}", f"    two: {q(two)}"]
    if design_prompt:
        L += ["design_note_prompt: |", block(design_prompt, 2)]
    L.append("ai_assisted: true")
    open(f"{d}/project.yaml", "w").write("\n".join(L) + "\n")
    open(f"{d}/starter/Main.java", "w").write(code(starter))
    open(f"{d}/solution/Main.java", "w").write(code(solution))
    for name, text in wrongs.items():
        open(f"{d}/wrong/{name}.java", "w").write(code(text))
