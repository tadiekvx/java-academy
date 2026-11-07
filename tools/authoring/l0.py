import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-0"
from build import *
import re

# ---------------- 0.1 ----------------
Lesson("j0-l0.1", "What Java is made of", ["J0.01"], [
    ("o1", "Describe the path from a .java source file to a running program: compile, then run"),
    ("o2", "Say what the JDK contains and why you need it, not just something that runs Java"),
    ("o3", "Explain what the java command does when you give it a .java file directly"),
], [], 25, ["I2", "I1"], r'''
## Before you start

This lesson is optional for now. Everything in Stage 1 runs in your browser, so you can start there and come back here when you want to write Java on your own computer. You'll want it before Stage 2.

You don't need to install anything to read this lesson.

## Explanation

Until now you've pressed **Run** and a program ran. This course's runner did several steps for you. On your own computer, you'll do them yourself, so it helps to know what they are.

### Source, bytecode, running

You write a **source file**, a text file ending in `.java`, like this one:

```java
void main() {
    IO.println("Hi");
}
```

A computer's processor can't run that directly. Java turns it into something else in two stages:

1. **Compile.** A program called the **compiler** (`javac`) reads your source, checks it for errors (the compile errors from [Errors are feedback](j1-l1.2)), and writes a **class file**, such as `Hello.class`, containing **bytecode**: instructions for an imaginary computer.
2. **Run.** The **Java Virtual Machine**, or **JVM** (started by the `java` command), reads the class file and carries out the bytecode on your real computer.

| Step | Tool | Reads | Produces |
|---|---|---|---|
| Compile | `javac` | `Hello.java` | `Hello.class` |
| Run | `java` | `Hello.class` | what your program prints |

The same bytecode runs on any computer with a JVM, which is why Java programs run the same on Windows, macOS and Linux.

### The JDK

To compile and run Java you install a **JDK**, a *Java Development Kit*. It contains `javac` (the compiler), `java` (which starts the JVM), the standard library you've been using (`String`, `ArrayList`, `IO`) and other tools. A download that only lets you *run* Java programs, without the compiler, isn't enough to follow this course, so check that what you install includes `javac`. You'll check that in the next lesson.

There are several JDK builds from different organisations (Eclipse Temurin, Oracle, Amazon Corretto, Microsoft and others). They are all built from the same open-source project, OpenJDK, and are interchangeable for this course.

### Version numbers

Java releases a new version every six months, and every few years one is marked **LTS**, *long-term support*, meaning it gets updates for longer. This course uses **Java 25**, an LTS release. The number you'll see most is the **major version**, `25`; any digits after it, like `25.0.5`, are update releases of version 25.

### A shortcut: running a source file directly

Compiling and then running is two commands. For a single file, `java` can do both at once:

```
java Hello.java
```

Given a **`.java`** file, `java` compiles it in memory, runs it straight away, and **leaves no class file behind**. This is how a small program or a script runs most simply, and it's what the compact `void main()` style was designed for. For anything bigger (several files, or a program you want to run many times), you compile properly. You'll try both in lesson 0.3.

## Worked examples

### Example 1: what happens to a file

*Task: you have `Notes.java`. Say what you'd do to run it, and what you'd have afterwards.*

**Step 1 — Is it a `.java` or a `.class` file?** `.java`: it's source, so it hasn't been compiled.

**Step 2 — Choose a route.** Two commands: `javac Notes.java`, then `java Notes`. Or one: `java Notes.java`.

**Step 3 — Say what's left behind.** After the two commands, `Notes.class` exists next to `Notes.java`. After the one command, only `Notes.java`.

### Example 2: reading the pieces of a version line

*Task: what does `javac 25.0.5` tell you?*

**Step 1 — Which tool is it?** `javac`: the compiler. So the compiler is installed.

**Step 2 — Which version?** 25: the major version, an LTS release, the one this course uses. The `.0.5` is the update number.

## Where this is used

- **Every Java project** has a compile step, usually run by a build tool such as Maven or Gradle that calls `javac` for you (Stage 4).
- **Servers** run class files (usually packaged together in a `.jar`), without the source.
- **Knowing the layers** helps when something goes wrong: "does it fail to compile, or fail to run?" is the first question asked of any Java problem.

## Common mistakes

### Thinking you can run a `.java` file with `javac`

`javac` only compiles; it doesn't run anything. To run, use `java`.

### Thinking `java Hello.class` is the way to run a class

You give `java` the **class name**, with no extension: `java Hello`. (Giving it the `.class` file name fails: you'll see the error in lesson 0.3.)

### Installing a runtime without the compiler

If `javac` isn't available, you have something that can run Java but not compile it. Install a JDK.

## Practice

::exercise{id=j0-l0.1-write-nextstep}

::exercise{id=j0-l0.1-explain-pipeline}

::exercise{id=j0-l0.1-explain-launcher}

## Further reading

- **JEP 512: Compact Source Files and Instance Main Methods** `[I2]`: describes the source-file launcher and why the compact style was added, in its own words.

## How you'll be assessed

- The **write** exercise checks that you know which tool comes next for each kind of file (*implementation*).
- The **explain** exercises check that you can describe the route from source to running program, what the JDK contains, and what `java File.java` does (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''', features=[("source-file launcher", 11)], resources=["jep-512"] if False else None) if False else None
