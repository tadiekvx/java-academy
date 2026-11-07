import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-0"
from build import *

# ======================= 0.3 =======================
Lesson("j0-l0.3", "Running Java from the terminal", ["J0.01"], [
    ("o1", "Run a program two ways: java File.java, and javac then java ClassName"),
    ("o2", "Write the same program in the traditional class form, and convert between the two forms"),
    ("o3", "Read the common launcher and compiler errors and say what causes each"),
], ["j0-l0.2"], 35, ["I2"], r'''
## Before you start

You should have a working JDK (`java -version` and `javac -version` both show 25, from [Installing a JDK](j0-l0.2)).

**Quick check.** Which of these leaves a `.class` file behind: `java Hello.java`, or `javac Hello.java`?

<details><summary>Show the answer</summary>

`javac Hello.java`. The `java Hello.java` shortcut compiles in memory and leaves no class file.

</details>

## Explanation

Open a terminal in the folder where your file lives. (How to open one in a folder depends on your system; your system's documentation or the IDE's terminal will show you.) Make a file called `Hello.java` containing:

```java
void main() {
    IO.println("Hi");
}
```

### Way 1: run the source file

```
java Hello.java
```

This prints `Hi`, and no class file appears: the folder still holds just `Hello.java`.

### Way 2: compile, then run

```
javac Hello.java
java Hello
```

`javac` produces `Hello.class` and prints nothing if all is well. `java Hello` runs it and prints `Hi`. Notice the second command gives the **class name**, `Hello`, **not** a file name.

### The traditional form

Almost all existing Java code, including every tutorial from before Java 25, writes the same program with a class around it:

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hi");
    }
}
```

| Compact (Java 25) | Traditional |
|---|---|
| `void main() { … }` | `public class Hello { public static void main(String[] args) { … } }` |
| `IO.println("Hi");` | `System.out.println("Hi");` |

Both do the same thing, and you need to read both. In the traditional form:

- The code lives in a **class**, and a **`public` class must be in a file of the same name**: `public class Hello` goes in `Hello.java`.
- The starting point is `public static void main(String[] args)`. You'll learn what each word means in Stage 2; for now, copy the line exactly.
- `System.out.println` is the traditional way to print; `System.out.print` is the same as `IO.print`.

### Reading the errors

These are the errors you'll meet. They were captured from a real Java 25 install.

**1. Giving `java` a class file name:**

```
java Hello.class
Error: Could not find or load main class Hello.class
Caused by: java.lang.ClassNotFoundException: Hello.class
```

Cause: `java` wants the class name, `Hello`, with no extension.

**2. A public class in a file with a different name:**

```
Hello2.java:1: error: class Greeter is public, should be declared in a file named Greeter.java
public class Greeter {
       ^
```

Cause: the file `Hello2.java` holds `public class Greeter`. Rename the file to `Greeter.java`, or rename the class to `Hello2`.

**3. A class with no `main`:**

```
Error: Main method not found in class Nope, please define the main method as:
   public static void main(String[] args)
or a JavaFX application class must extend javafx.application.Application
```

Cause: there's no starting method for `java` to call. (Ignore the JavaFX part; it's for a different kind of program.)

**4. A file that isn't there:**

```
java Missing.java
Error: Could not find or load main class Missing.java
```

Cause: no file of that name in the current folder. Check the folder you're in, and the spelling.

On some systems (macOS, Windows) file names aren't case-sensitive, but Java's class names are: running `java hello` when the class is `Hello` can fail with a message that mentions `wrong name`. Use exactly the same capitals as the class.

## Worked examples

### Example 1: compile and run, step by step

*Task: you have `Greeting.java` and want to run it the two-step way.*

**Step 1 — Compile:** `javac Greeting.java`. No message means it compiled. Compile errors would appear here, with a line number.

**Step 2 — Look for the class file:** `Greeting.class` is now in the folder.

**Step 3 — Run, by class name:** `java Greeting`.

### Example 2: converting a program to the traditional form

*Task: rewrite this in the traditional form.*

```java
void main() {
    IO.println("Total: " + (2 + 3));
}
```

**Step 1 — Wrap it in a class named after the file** (say the file is `Main.java`): `public class Main { … }`.

**Step 2 — Give the body a traditional `main` header:** `public static void main(String[] args) { … }`.

**Step 3 — Replace `IO.println` with `System.out.println`.**

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Total: " + (2 + 3));
    }
}
```

## Where this is used

- **Build tools and servers** run Java from the command line all the time, so reading these errors is routine.
- **Most existing Java** you'll read uses the traditional form, so you'll convert between the two forms constantly.
- **Reading an error and saying which of the four it is** is the first thing a colleague will ask you to do.

## Common mistakes

### `java Hello.class`

Use `java Hello`.

### Class name and file name disagree

A `public` class named `Greeter` must live in `Greeter.java`.

### Forgetting you're in the wrong folder

If a file "isn't found", check where your terminal is. The `ls` command (macOS/Linux) or `dir` (Windows) lists the files in the current folder.

## Practice

::exercise{id=j0-l0.3-write-classic}

::exercise{id=j0-l0.3-modify-compact}

::exercise{id=j0-l0.3-debug-filename}

::exercise{id=j0-l0.3-explain-errors}

## Further reading

- **JEP 512** `[I2]` explains how the launcher treats a source file, and the compact form.

## How you'll be assessed

- The **write**, **modify** and **debug** exercises check that you can write the traditional form, convert to the compact form, and fix a file-name mismatch. They check the **form** of your code as well as its output.
- The **explain** exercise checks that you can read launcher errors.

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''', resources=["jep-512"])

ex = Exercises("j0-l0.3")
CLASSIC_MAIN = "public static void main("
ex.io("write", "j0-l0.3-write-classic", "Write it with a class", ["o2"], ["J0.01"], ["IMPL"],
    "This compact program prints a greeting. Rewrite it in the **traditional form**: a `public class Main` containing `public static void main(String[] args)`, printing with `System.out.println`. It must print exactly the same text.",
    lambda s: "Hello from a class!", [("prints the greeting", "")], [],
    'void main() {\n    IO.println("Hello from a class!");\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello from a class!");\n    }\n}\n',
    {"still-compact": 'void main() {\n    IO.println("Hello from a class!");\n}\n',
     "class-but-wrong-printing": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello from a class");\n    }\n}\n'},
    ("Wrap the code in a class named Main, and give it the traditional main header. Don't forget System.out.println.", "public class Main { public static void main(String[] args) { System.out.println(\"Hello from a class!\"); } }"),
    source_tests=[("uses a public class Main", ["public class Main"], None), ("uses the traditional main method", [CLASSIC_MAIN], None), ("prints with System.out", ["System.out.println"], ["IO.println"])],
    difficulty=2)
ex.io("modify", "j0-l0.3-modify-compact", "Back to the compact form", ["o2"], ["J0.01"], ["MOD"],
    "This program is written in the traditional form. Convert it to the **compact form**: no class, a plain `void main()`, and `IO.println`. It must print exactly the same two lines.",
    lambda s: "Total: 5\nDone", [("prints both lines", "")], [],
    'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Total: " + (2 + 3));\n        System.out.println("Done");\n    }\n}\n',
    'void main() {\n    IO.println("Total: " + (2 + 3));\n    IO.println("Done");\n}\n',
    {"only-one-line": 'void main() {\n    IO.println("Total: " + (2 + 3));\n}\n',
     "class-kept": 'public class Main {\n    void main() {\n        IO.println("Total: " + (2 + 3));\n        IO.println("Done");\n    }\n}\n'},
    ("Remove the class wrapper and the old main header, then swap System.out.println for IO.println.", "void main() { IO.println(\"Total: \" + (2 + 3)); IO.println(\"Done\"); }"),
    source_tests=[("compact main", ["void main()"], ["public class", "System.out"]), ("uses IO", ["IO.println"], None)], difficulty=2)
ex.io("debug", "j0-l0.3-debug-filename", "The class in the wrong file", ["o3"], ["J0.01"], ["DEBUG"],
    "This program lives in the file `Main.java`, but it won't compile. Read the error, and fix it so that the program prints `Fixed!`.",
    lambda s: "Fixed!", [("prints Fixed!", "")], [],
    'public class Greeter {\n    public static void main(String[] args) {\n        System.out.println("Fixed!");\n    }\n}\n',
    'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Fixed!");\n    }\n}\n',
    {"changed-the-text": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Fixed");\n    }\n}\n'},
    ("Read the error: which two names disagree?", "A public class must be named after its file: rename Greeter to Main."),
    starter_compiles=False)
ex.explain("j0-l0.3-explain-errors", "Which error is this?", ["o3", "o1"], ["J0.01"],
    "A learner types `java Hello.class` and sees: `Error: Could not find or load main class Hello.class`. A second learner compiles `Hello2.java`, which holds `public class Greeter`, and sees: `class Greeter is public, should be declared in a file named Greeter.java`. For each, say what the mistake is and exactly what to type or change instead.",
    "A full answer says the first learner gave java a file name instead of a class name and should type java Hello; and that the second has a public class whose name doesn't match its file, so should rename the file to Greeter.java or the class to Hello2.",
    {2: ("Correctly diagnoses both: java needs the class name (java Hello, no .class), and a public class must match its file name, so rename the file to Greeter.java or the class to Hello2.",
         ["The first typed the file name; java wants the class name, so java Hello. The second has public class Greeter in Hello2.java, but a public class has to be in a file with its own name, so rename the file to Greeter.java or change the class to Hello2.",
          "java Hello.class is wrong because java takes a class name, not a file, so it should be java Hello. In the other, the class name and file name don't match, so rename one of them to match."]),
     1: ("Diagnoses one error correctly, or gives the cause without saying what to type or change.",
         ["The first should use java Hello.", "The class and the file name have to match."]),
     0: ("Incorrect, for example blames the install or says to add a semicolon.",
         ["Reinstall Java.", "Both are missing semicolons."])})

# ======================= 0.4 =======================
Lesson("j0-l0.4", "Your first IDE project", ["J0.01"], [
    ("o1", "Create a project in an IDE (IntelliJ IDEA or VS Code), run a program, and read errors in the editor"),
    ("o2", "Read a project's folder layout and say where the source and compiled files are"),
    ("o3", "Use a breakpoint to pause a running program and look at its variables"),
], ["j0-l0.3"], 30, ["I23", "I24"], r'''
## Before you start

You should be comfortable with the terminal route ([Running Java from the terminal](j0-l0.3)). An IDE does the same compile and run steps for you, and adds help while you type.

**Quick check.** What does `javac Main.java` produce?

<details><summary>Show the answer</summary>

`Main.class`, the bytecode, if the program compiles without errors.

</details>

## Explanation

### What an IDE is

An **IDE**, an *integrated development environment*, is an editor that also knows Java. It underlines errors as you type (using the same compiler messages you've been reading), completes names, runs your program with a button, and lets you pause it to look inside. Professional Java developers use one every day.

Two free choices work well for this course:

- **IntelliJ IDEA** is the most widely used Java IDE. Since version 2025.3 there is a single download. Its core Java and Kotlin features are free; paid features are unlocked with a subscription, and you get a 30-day trial of them, after which the free core keeps working.
- **Visual Studio Code** with the **Extension Pack for Java** is a lighter free editor with Java support added. Microsoft's tutorial recommends an all-in-one Coding Pack on Windows and macOS; on Linux you install the JDK, VS Code and the extensions separately.

Both need a JDK installed (you have one from lesson 0.2), and both can find it. **Menus and buttons change between versions**, so follow the current vendor tutorial linked below for the exact clicks, and use this lesson for what each step is *for*.

### What you do in an IDE

1. **Create a project.** A project is a folder the IDE manages: your source files, and settings such as which JDK to use. Choose Java 25 when it asks.
2. **Add a file.** Create `Main.java` in the project's **source folder**, often named `src`.
3. **Run it.** Use the **Run** button next to `main`. The IDE compiles and runs, and shows the output in a panel.
4. **Read the editor's feedback.** A red underline is a compile error, with the same message `javac` would print. Hover over it to read it.

### Reading a project layout

A small project might look like this:

```
my-first-project/
  src/
    Main.java
    Counter.java
  out/
    Main.class
    Counter.class
```

- `src` holds the **source** you write. `Main.java` has `main`, so that's where you run from.
- The IDE puts the **compiled** class files in an output folder. Its name varies (`out`, `bin` and `target` are all common); you don't edit anything in it.
- If `Counter.java` weren't in `src`, the compiler wouldn't find it.

### Breakpoints: pausing a running program

A **breakpoint** is a marker on a line of code. When you run the program in **debug mode** (VS Code: press F5 or Run, then Start Debugging), it **pauses** just before that line. While it's paused you can:

- look at the **value of every variable** at that moment;
- **step** one line at a time and watch the values change.

This is a live version of the trace tables from [Tracing loops](j1-l4.2). It's the best way to answer "what is the program actually doing?". You'll use it properly in Stage 4.

## Worked examples

### Example 1: finding a bug with a breakpoint

*Task: `total` ends up wrong in a loop. How would a breakpoint help?*

```java
int total = 0;
for (int i = 0; i <= 3; i++) {
    total += i * 10;       // put a breakpoint on this line
}
```

**Step 1 — Put the breakpoint on the line inside the loop.**

**Step 2 — Run in debug mode.** It pauses the first time that line is reached: `i` is 0, `total` is 0.

**Step 3 — Continue, and watch.** Each time, check `i` and `total`: 0, 10, 20, 30. You can see the loop runs for `i` = 0, 1, 2 **and 3**, because of `<=`: an off-by-one you can now see rather than guess.

### Example 2: reading a layout

*Task: in the layout above, you edit `Counter.java`, run, and nothing changes. What might be wrong?*

**Step 1 — Which folder did you edit?** If you edited a copy in `out`, the IDE recompiles from `src` and overwrites it.

**Step 2 — Fix:** only edit files in `src`.

## Where this is used

- **Every professional Java developer** works in an IDE, mostly for the debugger, the instant error feedback, and navigating big projects.
- **A project's folder layout** is the first thing you look at in unfamiliar code.
- **Breakpoints** are how most bugs get found in real systems.

## Common mistakes

### Editing the output folder

The compiled files are regenerated. Edit only your source files.

### Running with the wrong JDK

If the IDE's project is set to an older JDK, your Java 25 code won't compile. Check the project's JDK setting first.

### Treating red underlines as noise

They're the compiler's messages arriving early. Read them as you would an error from `javac`.

## Practice

::exercise{id=j0-l0.4-explain-layout}

::exercise{id=j0-l0.4-explain-firstrun}

## Further reading

- **Getting Started with Java in VS Code** `[I23]` and **IntelliJ IDEA as a unified product** `[I24]`: the current vendor pages for each IDE.

## How you'll be assessed

- The **explain** exercises check that you can read a project layout, describe the steps of creating and running a project, and say what a breakpoint lets you see (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''', resources=["vscode-java-tutorial", "intellij-free-core"])

ex = Exercises("j0-l0.4")
ex.explain("j0-l0.4-explain-layout", "Read the layout", ["o2"], ["J0.01"],
    "Here is a project's layout:\n\n```\nshop/\n  src/\n    Main.java\n    Basket.java\n  out/\n    Main.class\n    Basket.class\n```\n\nWhich file would you run to start the program, and how do you know? Where is the code you edit, and what is in the `out` folder? A colleague has been editing `out/Basket.class`: what should they do instead, and why?",
    "A full answer says Main.java is run because it holds main (the starting point); the editable source is in src; out holds compiled class files generated by the IDE; edit the .java source in src, because the class files are regenerated when the project is compiled.",
    {2: ("Says Main.java is the one to run (it has main), the source in src is what you edit, out holds generated compiled class files, and the colleague should edit the .java in src because out is overwritten on compile.",
         ["I'd run Main.java because it has the main method. The code I edit is in src; out has the compiled .class files, which the IDE generates. The colleague should edit Basket.java in src, since out gets regenerated and their changes would be lost.",
          "Main.java is the entry point. src is source, out is compiled output. They shouldn't edit a .class file, but the .java in src, because the IDE recompiles and replaces the output."]),
     1: ("Gets part of it: identifies Main.java, or says edit src, but misses why the output folder shouldn't be edited.",
         ["Run Main.java.", "They should edit src instead."]),
     0: ("Incorrect, for example says to edit the class files, or that out holds the source.",
         ["Edit the class files in out.", "out is where the source is."])})
ex.explain("j0-l0.4-explain-firstrun", "Your first run, and a breakpoint", ["o1", "o3"], ["J0.01"],
    "Describe the steps to create a project in your IDE and run a program, in your own words. Then explain what a breakpoint lets you do that just pressing Run does not, and give an example of a bug it would help you find.",
    "A full answer lists create a project with the right JDK, add a Java file in the source folder, press Run and read the output and any red-underline errors; and explains a breakpoint pauses the running program at a line so you can see variable values and step through, e.g. finding an off-by-one in a loop.",
    {2: ("Gives the steps (create a project with Java 25, add a file in the source folder, run it, read errors) and explains that a breakpoint pauses the program so you can inspect variables and step, with a sensible bug example such as an off-by-one in a loop.",
         ["Create a project and choose the Java 25 JDK, add Main.java in src, press Run and look at the output panel and any red underlines. A breakpoint pauses the program at a line so I can see the variables and step one line at a time. I could use it to see why a loop runs one time too many.",
          "New project with the right JDK, new Main.java, Run. Red underlines are compile errors. With a breakpoint in debug mode the program stops there and I can check what each variable holds, like seeing that total is wrong after the third pass of a loop."]),
     1: ("Gives the steps or explains breakpoints, but not both, or the breakpoint example is missing.",
         ["Make a project, make a file, press run.", "A breakpoint pauses the program."]),
     0: ("Incorrect, for example says a breakpoint fixes bugs automatically, or says to run it from the output folder.",
         ["A breakpoint fixes the bug for you.", "Open the out folder and double-click the class file."])})
print("0.3, 0.4 written")
