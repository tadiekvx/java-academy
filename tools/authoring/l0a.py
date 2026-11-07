import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-0"
from build import *

# ======================= 0.1 =======================
Lesson("j0-l0.1", "What Java is made of", ["J0.01"], [
    ("o1", "Describe the path from a .java source file to a running program: compile, then run"),
    ("o2", "Say what the JDK contains, and why you need one rather than something that only runs Java"),
    ("o3", "Explain what the java command does when you give it a .java file directly"),
], [], 25, ["I2", "I1"], r'''
## Before you start

This lesson is **optional for now**. Everything in Stage 1 runs in your browser, so you can start there and come back here when you want to write Java on your own computer. You'll want it before Stage 2.

You don't need to install anything to read this lesson.

## Explanation

Until now you've pressed **Run** and a program ran. This course's runner did several steps for you. On your own computer you'll do them yourself, so it helps to know what they are.

### Source, bytecode, running

You write a **source file**, a text file ending in `.java`:

```java
void main() {
    IO.println("Hi");
}
```

A computer's processor can't run that directly. Java turns it into something it can run in two stages:

1. **Compile.** A program called the **compiler**, `javac`, reads your source and checks it for errors (the compile errors from [Errors are feedback](j1-l1.2)). If it's fine, it writes a **class file** such as `Hello.class`, containing **bytecode**: instructions for an imaginary computer.
2. **Run.** The **Java Virtual Machine**, or **JVM**, started by the `java` command, reads the class file and carries out the bytecode on your real computer.

| Step | Tool | Reads | Produces |
|---|---|---|---|
| Compile | `javac` | `Hello.java` | `Hello.class` |
| Run | `java` | the class `Hello` | what your program prints |

The same bytecode runs on any computer that has a JVM, which is why Java programs behave the same on Windows, macOS and Linux.

### The JDK

To compile and run Java you install a **JDK**, a *Java Development Kit*. It contains `javac` (the compiler), `java` (which starts the JVM), the standard library you've been using (`String`, `ArrayList`, `IO`) and other tools. Something that only runs Java programs, without the compiler, isn't enough to follow this course, so check that what you install includes `javac`. You'll check that in the next lesson.

There are several JDK builds from different organisations: Eclipse Temurin, Oracle, Amazon Corretto, Microsoft and others. They're built from the same open-source project, OpenJDK, and any of them works for this course.

### Version numbers

Java releases a new version every six months, and every few years one is marked **LTS**, *long-term support*, meaning it gets updates for longer. This course uses **Java 25**, an LTS release. The number you'll see most is the **major version**, `25`. Digits after it, like `25.0.5`, are update releases of version 25.

### A shortcut: running a source file directly

Compiling and then running is two commands. For a single file, `java` can do both at once:

```
java Hello.java
```

Given a **`.java`** file, `java` compiles it in memory, runs it straight away, and leaves **no class file** behind. That's the simplest way to run a small program or a script, and it's what the compact `void main()` style was designed for. For anything bigger (several files, or a program you'll run many times), you compile properly. You'll try both in lesson 0.3.

## Worked examples

### Example 1: what happens to a file

*Task: you have `Notes.java`. Say how you'd run it, and what you'd have afterwards.*

**Step 1 — Is it a `.java` or a `.class` file?** `.java`: it's source, so it hasn't been compiled.

**Step 2 — Choose a route.** Two commands: `javac Notes.java`, then `java Notes`. Or one command: `java Notes.java`.

**Step 3 — Say what's left behind.** After the two commands, `Notes.class` sits next to `Notes.java`. After the single command, only `Notes.java`.

### Example 2: reading a version line

*Task: what does `javac 25.0.5` tell you?*

**Step 1 — Which tool answered?** `javac`: the compiler is installed, so you have a JDK, not just a runtime.

**Step 2 — Which version?** 25 is the major version, an LTS release, the one this course uses. The `.0.5` is the update number.

## Where this is used

- **Every Java project** has a compile step. Build tools such as Maven and Gradle (Stage 4) call `javac` for you.
- **Servers** run class files, usually bundled in a `.jar`, without the source.
- **"Does it fail to compile, or fail to run?"** is the first question asked about any Java problem. Knowing the two steps lets you answer it.

## Common mistakes

### Trying to run a source file with `javac`

`javac` only compiles; it prints nothing from your program. To run, use `java`.

### Giving `java` a class file name

You give `java` the **class name**, with no extension: `java Hello`, not `java Hello.class`. Lesson 0.3 shows the error you get.

### Installing a runtime without the compiler

If the `javac` command isn't found, you have something that can run Java but not compile it. Install a JDK.

## Practice

::exercise{id=j0-l0.1-write-nextstep}

::exercise{id=j0-l0.1-explain-pipeline}

::exercise{id=j0-l0.1-explain-launcher}

## Further reading

- **JEP 512: Compact Source Files and Instance Main Methods** `[I2]`: the official description of why Java 25 lets a first program be just `void main()`, in the project's own words.

## How you'll be assessed

- The **write** exercise checks that you know which tool comes next for each kind of file (*implementation*).
- The **explain** exercises check that you can describe the route from source to running program, what the JDK contains, and what `java File.java` does (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''', features=[("source-file launcher", 11)], resources=["jep-512", "adoptium-install"])

ex = Exercises("j0-l0.1")
def next_step(f):
    if f.endswith(".java"): return "javac " + f
    if f.endswith(".class"): return "java " + f[:-6]
    return "unknown"
NS_H = [(None, ["Main.java"], "another source file"), (None, ["Main.class"], "another class file"), (None, ["readme.md"], "a markdown file"),
        (None, ["Program.class"], "a longer name"), (None, ["a.b.java"], "a dot in the name"), (None, ["java"], "just the word java"), (None, ["Hello.JAVA"], "capitals matter")]
ex.method("write", "j0-l0.1-write-nextstep", "Which command next?", ["o1"], ["J0.01"], ["IMPL"],
    "Write a method called `nextStep` that is given a file name and returns the command that moves it forward:\n\n- a name ending in `.java` returns `javac ` followed by the file name (compile it), e.g. `javac Hello.java`;\n- a name ending in `.class` returns `java ` followed by the **class name**, which is the file name without `.class`, e.g. `java Hello`;\n- anything else returns `unknown`.\n\nFile extensions are case-sensitive here: `Hello.JAVA` is unknown.",
    [("nextStep", [("fileName", "String")], "String")], {"nextStep": next_step},
    [(None, ["Hello.java"]), (None, ["Hello.class"]), (None, ["notes.txt"])], NS_H,
    '// Write the nextStep method here.\n\nvoid main() {\n    IO.println(nextStep("Hello.java")); // should print javac Hello.java\n}\n',
    'String nextStep(String fileName) {\n    if (fileName.endsWith(".java")) {\n        return "javac " + fileName;\n    }\n    if (fileName.endsWith(".class")) {\n        return "java " + fileName.substring(0, fileName.length() - ".class".length());\n    }\n    return "unknown";\n}\n\nvoid main() {\n    IO.println(nextStep("Hello.java")); // should print javac Hello.java\n}\n',
    {"keeps-extension": 'String nextStep(String fileName) {\n    if (fileName.endsWith(".java")) {\n        return "javac " + fileName;\n    }\n    if (fileName.endsWith(".class")) {\n        return "java " + fileName;\n    }\n    return "unknown";\n}\n\nvoid main() {\n}\n',
     "ignores-case": 'String nextStep(String fileName) {\n    if (fileName.toLowerCase().endsWith(".java")) {\n        return "javac " + fileName;\n    }\n    if (fileName.endsWith(".class")) {\n        return "java " + fileName.substring(0, fileName.length() - 6);\n    }\n    return "unknown";\n}\n\nvoid main() {\n}\n'},
    ("endsWith tells you how a name ends. For .class, which part of the name do you keep?", "Compile .java files with \"javac \" + name; for .class files, use substring to drop the last 6 characters."),
    starter_compiles=False)
ex.explain("j0-l0.1-explain-pipeline", "From source to running", ["o1", "o2"], ["J0.01"],
    "Explain, in your own words, what happens between writing `Hello.java` and seeing its output on screen. Name the two tools, the file each one produces or reads, and say what a JDK contains.",
    "A full answer names the compiler (javac) turning Hello.java into a Hello.class file of bytecode, and the java command / JVM running that class; and says a JDK contains the compiler and the runtime/library (javac, java and the standard library).",
    {2: ("Names javac compiling the .java source into a .class bytecode file, the java command (JVM) then running it, and says the JDK includes javac, java and the standard library.",
         ["javac compiles Hello.java into Hello.class, which is bytecode. Then the java command starts the JVM, which runs that bytecode. The JDK is the kit that has both javac and java plus the standard library.",
          "First you compile with javac, producing a .class file. Then java Hello runs it on the JVM. A JDK contains the compiler, the runtime and the library, so you can do both."]),
     1: ("Gets the compile-then-run order, or names one tool, but misses what is produced or what the JDK contains.",
         ["You compile it and then run it.", "javac makes a class file and java runs it."]),
     0: ("Incorrect or confused, for example says java compiles and javac runs, or that the class file is the source.",
         ["java compiles it and javac runs it.", "The .class file is what you write."])})
ex.explain("j0-l0.1-explain-launcher", "What does java Hello.java do?", ["o3"], ["J0.01"],
    "You type `java Hello.java` (with the `.java`). What does the java command do, and what files exist afterwards? Why is this convenient for a small program, and why isn't it enough for a bigger one?",
    "A full answer says java compiles the source in memory and runs it straight away, leaving no .class file; convenient because it's one command for a single small file; not enough for bigger programs with several files or that should be compiled once and run many times.",
    {2: ("Says the source is compiled in memory and run at once, with no class file left behind, and gives one reason it suits small programs and one why bigger programs need a proper compile.",
         ["It compiles Hello.java in memory and runs it straight away, so no Hello.class is created. That's quick for a small single-file program, but with lots of files you need to compile properly, and you'd rather not recompile every time you run.",
          "java compiles and runs the file in one go and leaves only Hello.java. It's great for scripts, but a big program has many files and is compiled once into class files."]),
     1: ("Says it runs the file in one step but misses that no class file is left, or doesn't give a reason about bigger programs.",
         ["It compiles and runs it in one command.", "It runs the .java file directly without javac."]),
     0: ("Incorrect, for example says it needs javac first, or that it only works on class files.",
         ["You must run javac first, and then java Hello.java.", "It runs the .class file."])})

# ======================= 0.2 =======================
Lesson("j0-l0.2", "Installing a JDK and checking it", ["J0.01"], [
    ("o1", "Install a JDK and check the install with java -version and javac -version"),
    ("o2", "Read a version line and work out the major version"),
    ("o3", "Diagnose the common causes of the wrong Java version, or of command not found"),
], ["j0-l0.1"], 30, ["I22"], r'''
## Before you start

You should know what a JDK contains ([What Java is made of](j0-l0.1)). This lesson asks you to install software on your computer, so it's the first one where you'll do the work outside the browser.

**Quick check.** Which command compiles, and which runs?

<details><summary>Show the answer</summary>

`javac` compiles; `java` runs.

</details>

## Explanation

### Choosing a JDK

Any current build of **Java 25** will do. Eclipse Temurin, from the Eclipse Adoptium project, is a free, widely used choice with installers for Windows, macOS and Linux. Its installation page labels Java 25 as the latest LTS release, and recommends a package manager on most systems. (Other good builds are listed on your IDE's page too.) Pick one, download it for your system, and run the installer.

Each system has its own steps, and they change, so follow the instructions on the download page for your own computer rather than a recipe here. One example from that page: on Windows, with the `winget` package manager, the command for Java 25 is:

```
winget install EclipseAdoptium.Temurin.25.JDK
```

### Checking the install

Open a **terminal** (Terminal on macOS, a terminal on Linux, PowerShell or Command Prompt on Windows), **close and reopen it after installing** (so it notices the change), and type:

```
java -version
javac -version
```

You should see something like this (on one computer, a Homebrew build; yours will name your vendor and may show a different update number):

```
openjdk version "25.0.5.0.3" 2026-10-24
OpenJDK Runtime Environment Homebrew (build 25.0.5.0.3)
OpenJDK 64-Bit Server VM Homebrew (build 25.0.5.0.3, mixed mode, sharing)
javac 25.0.5.0.3
```

Read it:

- The **first line** has the **major version** in quotes: `"25.0.5.0.3"` is version **25**. Older Java used `1.8.0_292` for Java **8**: when the number starts with `1.`, the major version is the number after it.
- The next lines name the **runtime** (`java`) and the **virtual machine**. The vendor's name appears in the middle.
- The last line is `javac`: **if it prints a version, you have the compiler**, so you installed a JDK.

You need both commands to answer with major version **25**.

### When it goes wrong

| What you see | Usual cause | What to do |
|---|---|---|
| `command not found` (macOS/Linux) or `'java' is not recognized` (Windows) | The install isn't on your **PATH**, the list of folders the terminal searches for commands; or you didn't reopen the terminal | Reopen the terminal; re-run the installer and look for an option to add Java to the PATH; check the vendor's instructions |
| `java -version` works, `javac -version` says not found | You have a runtime without the compiler | Install a **JDK** |
| `java -version` shows an **older** version (17, 21, …) | An older Java is earlier in the PATH, or an old `JAVA_HOME` setting points at it | Find which `java` the terminal is using (`which java` on macOS/Linux, `where java` on Windows), and put the new one first or remove the old one |

**`JAVA_HOME`** is an optional setting that some tools use to find the JDK. If a tool says it can't find Java, or finds the wrong one, check what `JAVA_HOME` points at.

## Worked examples

### Example 1: reading a version line

*Task: what is the major version in `openjdk version "17.0.9" 2023-10-17`?*

**Step 1 — Find the number in quotes.** `17.0.9`.

**Step 2 — Does it start with `1.`?** No.

**Step 3 — Take the number before the first dot.** 17. This isn't Java 25, so you'd need to install or select a newer JDK.

### Example 2: diagnosing a wrong version

*Task: you installed Java 25, but `java -version` says 17. What's your plan?*

**Step 1 — Did you reopen the terminal?** An open terminal doesn't notice the new install.

**Step 2 — Find which `java` it's running.** `which java` or `where java` prints the path. If it points into an old Java's folder, the old one is first in your PATH.

**Step 3 — Fix the order, not just the install.** Move the new one first (or remove the old). Check again with both `java -version` and `javac -version`: they should agree.

## Where this is used

- **Every developer's first day** involves getting the right JDK installed. Several versions side by side is normal on a working machine.
- **Build tools** and **IDEs** each need to know which JDK to use, so you'll meet `JAVA_HOME` and version mismatches again.
- **Bug reports** usually start with "Java version: …". Being able to read the line is routine.

## Common mistakes

### Not reopening the terminal

The terminal reads the PATH when it starts. Open a new one after installing.

### Checking only `java -version`

`java` alone doesn't prove you have the compiler. Check `javac -version` too.

### Assuming `1.8` means 1.8

For old Java, `1.8.0_292` means Java **8**. From Java 9 on, the first number is the major version.

## Practice

::exercise{id=j0-l0.2-write-majorversion}

::exercise{id=j0-l0.2-explain-checks}

::exercise{id=j0-l0.2-explain-wrongversion}

## Further reading

- **Installing Eclipse Temurin** `[I22]`: the download and install page for one free JDK build, for all three operating systems.

## How you'll be assessed

- The **write** exercise checks that you can read a version line (*implementation*).
- The **explain** exercises check that you know how to verify an install, and how to diagnose a wrong version (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''', resources=["adoptium-install"])

def major(line):
    inner = line.split('"')[1]
    if inner.startswith("1."):
        inner = inner[2:]
    digits = ""
    for c in inner:
        if c.isdigit(): digits += c
        else: break
    return int(digits)
ex = Exercises("j0-l0.2")
ex.method("write", "j0-l0.2-write-majorversion", "Read the version", ["o2"], ["J0.01"], ["IMPL"],
    "Write a method called `majorVersion` that is given the **first line** printed by `java -version` and returns the major version as an `int`.\n\nThe version is the text between the double quotes. For modern versions the major version is the number before the first dot or other non-digit (`\"25.0.5\"` → 25, `\"21\"` → 21, `\"27-ea\"` → 27). For old Java versions that start with `1.` the major version is the number after it (`\"1.8.0_292\"` → 8).",
    [("majorVersion", [("line", "String")], "int")], {"majorVersion": major},
    [(None, ['openjdk version "25.0.5.0.3" 2026-10-24']), (None, ['java version "1.8.0_292"']), (None, ['openjdk version "17.0.9" 2023-10-17'])],
    [(None, ['openjdk version "21" 2023-09-19'], "no dots"), (None, ['openjdk version "27-ea" 2026-09-15'], "early access"), (None, ['java version "1.7.0_80"'], "Java 7"), (None, ['openjdk version "11.0.21" 2023-10-17 LTS'], "Java 11"),
     (None, ['java version "1.8"'], "old style without update"), (None, ['openjdk version "9.0.4"'], "Java 9"), (None, ['openjdk version "25.0.1" 2025-10-21 LTS'], "Java 25 LTS")],
    '// Write the majorVersion method here.\n\nvoid main() {\n    IO.println(majorVersion("openjdk version \\"25.0.5\\" 2026-10-24")); // should print 25\n}\n',
    'int majorVersion(String line) {\n    int start = line.indexOf(\'"\') + 1;\n    int end = line.indexOf(\'"\', start);\n    String version = line.substring(start, end);\n    if (version.startsWith("1.")) {\n        version = version.substring(2);\n    }\n    int digits = 0;\n    while (digits < version.length() && Character.isDigit(version.charAt(digits))) {\n        digits++;\n    }\n    return Integer.parseInt(version.substring(0, digits));\n}\n\nvoid main() {\n    IO.println(majorVersion("openjdk version \\"25.0.5\\" 2026-10-24")); // should print 25\n}\n',
    {"first-number-only": 'int majorVersion(String line) {\n    int start = line.indexOf(\'"\') + 1;\n    int end = line.indexOf(\'"\', start);\n    String version = line.substring(start, end);\n    int digits = 0;\n    while (digits < version.length() && Character.isDigit(version.charAt(digits))) {\n        digits++;\n    }\n    return Integer.parseInt(version.substring(0, digits));\n}\n\nvoid main() {\n}\n',
     "stops-at-first-dot": 'int majorVersion(String line) {\n    int start = line.indexOf(\'"\') + 1;\n    String version = line.substring(start);\n    int dot = version.indexOf(\'.\');\n    return Integer.parseInt(version.substring(0, dot));\n}\n\nvoid main() {\n}\n'},
    ("Find the text between the quotes first. Then handle the old '1.' style, and read only the leading digits.", "indexOf('\"') and substring to get the version; if it starts with \"1.\" drop those two characters; then take the leading digits and parseInt them."),
    starter_compiles=False, difficulty=3)
ex.explain("j0-l0.2-explain-checks", "How do you know it worked?", ["o1"], ["J0.01"],
    "You've just installed a JDK. Which commands do you run to check it worked, and what should each one show? Give your own results if you've installed it, or say what you expect to see. Say why you need to check more than one command.",
    "A full answer names java -version and javac -version (in a freshly opened terminal), says each should print a version with major version 25, and explains that checking javac proves the compiler is installed (a JDK), which java -version alone doesn't.",
    {2: ("Names both java -version and javac -version, says they should show major version 25, and explains that javac proves the compiler (JDK) is installed while java alone could be a runtime only.",
         ["I'd open a new terminal and run java -version and javac -version. Both should show 25. Checking javac matters because if it's missing I only have a runtime, not a JDK, so I couldn't compile.",
          "java -version should say 25 and javac -version should print javac 25.something. I need javac too because a runtime without the compiler isn't enough."]),
     1: ("Names the commands or the expected version, but doesn't explain why javac is checked as well.",
         ["java -version and javac -version.", "Run java -version and it should say 25."]),
     0: ("Incorrect or vague, for example only says to restart the computer, or names commands that don't exist.",
         ["Restart and see if Java is there.", "Run java --check."])})
ex.explain("j0-l0.2-explain-wrongversion", "Installed 25, but it says 17", ["o3"], ["J0.01"],
    "You installed Java 25, but `java -version` still says 17. List the likely causes in the order you'd check them, and what you'd do about each.",
    "A full answer lists: terminal not reopened after installing; an older java earlier on the PATH (find it with which java / where java and reorder or remove it); possibly an old JAVA_HOME pointing at the old JDK; and says to re-check both java -version and javac -version afterwards.",
    {2: ("Gives at least two correct causes with a check or fix for each (reopen the terminal; an old java earlier on the PATH, found with which/where; an old JAVA_HOME), and says to re-check.",
         ["First reopen the terminal in case it hasn't noticed. Then run which java (or where java) to see which one it's using; if it's the old one, put the new one first in the PATH or remove the old. Also check JAVA_HOME. Then run java -version and javac -version again.",
          "Probably the old Java is earlier in the PATH. I'd close and reopen the terminal, use where java to find which is running, fix the order, and check JAVA_HOME points at 25."]),
     1: ("Gives one correct cause or fix, or several without saying how to check.",
         ["The old one is probably first in the PATH.", "Reopen the terminal and try again."]),
     0: ("Incorrect, for example says to reinstall repeatedly, or that Java can't have two versions installed.",
         ["You can't have two versions, so uninstall the computer's Java.", "Reinstall Java 25 again and again."])})
print("0.1, 0.2 written")
