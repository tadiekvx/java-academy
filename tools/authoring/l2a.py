import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-2"
from build import *
import outline

STAMP = {}
def reg(lessons, misc):
    outline.register(lessons, misc)

# ====================================================================== 2.1.1
Lesson("j2-l1.1", "From main to a class", ["J2.01"], [
    ("o1", "Declare a class with fields and a constructor, and fix a constructor that doesn't store its values"),
    ("o2", "Create objects with new, read and change their fields, and predict what each object holds"),
    ("o3", "Explain the difference between a class and an object, and say what a constructor is for"),
], ["j1-l7.4"], 40, ["R8", "I2"], r'''
## Before you start

You should be comfortable with methods and arrays ([Parameters and return values](j1-l5.2), [Arrays](j1-l6.1)).

**Quick check.** A program needs to remember a student's name and their grade. With what you know so far, how would you store both?

<details><summary>Show the answer</summary>

Two separate variables (`String name; int grade;`), or two arrays that you keep in step by index. Either way, nothing says the two values belong together.

</details>

## Explanation

So far, every value in your programs has been a number, some text, a boolean, or an array of those. Real programs deal with **things**: a student, a bank account, a receipt. A thing has several related pieces of information, and Java lets you bundle them into your own type, called a **class**.

### A class is a blueprint, an object is one thing built from it

```java
class Student {
    String name;
    int grade;
}
```

This declares a new **type** called `Student`, with two **fields** (variables that belong to each student). It doesn't make a student yet. It describes what every student will have, like a blueprint describes every house built from it.

You make an actual student, an **object**, with `new`:

```java runnable
class Student {
    String name;
    int grade;
}

void main() {
    Student s = new Student();
    s.name = "Ada";
    s.grade = 90;
    IO.println(s.name + " has " + s.grade);
}
```

- `new Student()` builds one object in memory.
- `s` is a variable of type `Student` that lets you reach it.
- `s.name` means *the `name` field of the object `s` refers to*. The dot reads "of".

You can build as many objects as you like from one class, and **each has its own fields**:

```java
Student a = new Student();
Student b = new Student();
a.grade = 70;
b.grade = 95;     // a.grade is still 70
```

### Fields start with default values

If you don't give a field a value, Java does:

| Field type | Starts as |
|---|---|
| `int`, `double` | `0` / `0.0` |
| `boolean` | `false` |
| `String` and every other object type | `null` (nothing there) |

This is different from local variables, which have no default and must be given a value before use.

### Constructors: setting up an object properly

Writing `new Student()` and then filling in each field by hand is easy to forget. A **constructor** is a special method that runs when you write `new`, so the object is ready to use straight away:

```java
class Student {
    String name;
    int grade;

    Student(String name, int grade) {
        this.name = name;
        this.grade = grade;
    }
}
```

- It has **the same name as the class** and **no return type** (not even `void`).
- You call it by passing arguments to `new`: `new Student("Ada", 90)`.
- Inside, `this.name` means *the field called `name` of the object being built*. A plain `name` means the **parameter**. When a parameter has the same name as a field, the parameter hides the field, so you need `this.` to reach the field.

If you write `name = name;` inside the constructor, you assign the parameter to itself and the field never changes. That compiles without any error, which makes it a tricky bug.

Once you write **any** constructor, Java stops providing the empty `new Student()` unless you write that too.

### Where classes go in a compact file

In a compact source file you can put classes beside `main`, as in the examples above. Java treats the loose methods as belonging to an implicitly declared class `[I2]`, and compiles the other classes in the same file along with it. In a traditional file the same code looks like this:

```java
public class Main {
    static class Student {          // 'static' here is explained in lesson 2.1.4
        String name;
        int grade;
    }
    public static void main(String[] args) {
        Student s = new Student();
    }
}
```

You'll read that form a lot in other people's code. Everything in this stage works in both.

## Worked examples

### Example 1: modelling a book

*Task: a library program needs books with a title and a page count, and it must be possible to create one in a single step.*

**Step 1 — Decide the fields.** `String title; int pages;`

**Step 2 — Write the constructor with the same two pieces of information,** and store each with `this.`.

**Step 3 — Build one and read it back.**

```java runnable
class Book {
    String title;
    int pages;

    Book(String title, int pages) {
        this.title = title;
        this.pages = pages;
    }
}

void main() {
    Book b = new Book("Dune", 612);
    IO.println(b.title + ", " + b.pages + " pages");
}
```

**Step 4 — Check.** It prints `Dune, 612 pages`.

### Example 2: finding a bug that compiles

*Task: this program prints `0 0`. Why?*

```java
class Point {
    int x;
    int y;
    Point(int x, int y) {
        x = x;
        y = y;
    }
}
```

**Step 1 — Look at what `x = x` does.** Both sides are the parameter, because the parameter hides the field.

**Step 2 — So the fields are never set,** and keep their default `0`.

**Step 3 — Fix it:** `this.x = x; this.y = y;`

## Predict, then run

::exercise{id=j2-l1.1-predict-objects}

## Where this is used

- **Every Java program of any size** is made of classes. The Brightbank application you'll build in this stage starts with an `Account` class.
- **Reading other people's code** is mostly reading classes: what are its fields, and how is it constructed?
- **Frameworks** create objects for you from classes you write, so understanding construction matters even when you don't type `new`.

## Common mistakes

:::mistake{id=MC27}
**Mixing up the class and an object.** `Student.name` doesn't mean anything: the class describes students, but only an object (`s.name`) holds a name.
:::

:::mistake{id=MC28}
**Writing `name = name;` in a constructor.** The parameter hides the field, so the field stays at its default. Write `this.name = name;`.
:::

:::mistake{id=MC29}
**Expecting a `String` field to start as an empty string.** It starts as `null`, and calling a method on it fails with a `NullPointerException`.
:::

## Practice

::exercise{id=j2-l1.1-write-book}

::exercise{id=j2-l1.1-write-student}

::exercise{id=j2-l1.1-debug-shadow}

::exercise{id=j2-l1.1-explain-class-object}

## Version notes

Compact source files, which let you put `void main()` and your classes in one file with no wrapper, arrived in **Java 25** `[I2]`. Everything about classes, fields and constructors is the same as in Java 1.0.

## Further reading

- **"Students' misconceptions and other difficulties in introductory programming"** (Qian & Lehman, 2017) `[R8]` covers how beginners understand objects, including confusing the class with its instances.
- **JEP 512** `[I2]` describes how a compact source file's loose methods become members of an implicitly declared class.

## How you'll be assessed

- The **write** and **debug** exercises check that you can declare a class with fields and a constructor, and fix one that doesn't store its values (*implementation, debugging*).
- The **predict** exercise checks that you know each object has its own fields and what default values look like (*identifying mistakes*).
- The **explain** exercise checks that you can say what a class, an object and a constructor are (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j2-l1.1")
ex.method("write", "j2-l1.1-write-book", "Model a book", ["o1"], ["J2.01"], ["IMPL"],
    "The driver `describeBook` at the bottom is finished. It uses a class called `Book` that you must write. A `Book` has a `String title` and an `int pages`, and a constructor that takes both, in that order, and stores them. Make `describeBook(\"Dune\", 612)` return `Dune (612 pages)`.",
    [("describeBook", [("title", "String"), ("pages", "int")], "String")],
    {"describeBook": lambda t, p: f"{t} ({p} pages)"},
    [("describeBook", ["Dune", 612]), ("describeBook", ["Emma", 474]), ("describeBook", ["Tiny", 1])],
    [("describeBook", ["", 0]), ("describeBook", ["A longer title here", 1000]), ("describeBook", ["x", 99]), ("describeBook", ["Ulysses", 730]), ("describeBook", ["Zero", 0])],
    '// Write the class Book here.\n\nString describeBook(String title, int pages) {\n    Book b = new Book(title, pages);\n    return b.title + " (" + b.pages + " pages)";\n}',
    'class Book {\n    String title;\n    int pages;\n\n    Book(String title, int pages) {\n        this.title = title;\n        this.pages = pages;\n    }\n}\n\nString describeBook(String title, int pages) {\n    Book b = new Book(title, pages);\n    return b.title + " (" + b.pages + " pages)";\n}',
    {"forgets-pages": 'class Book {\n    String title;\n    int pages;\n    Book(String title, int pages) {\n        this.title = title;\n    }\n}\n\nString describeBook(String title, int pages) {\n    Book b = new Book(title, pages);\n    return b.title + " (" + b.pages + " pages)";\n}',
     "forgets-title": 'class Book {\n    String title;\n    int pages;\n    Book(String title, int pages) {\n        this.pages = pages;\n    }\n}\n\nString describeBook(String title, int pages) {\n    Book b = new Book(title, pages);\n    return b.title + " (" + b.pages + " pages)";\n}'},
    ("The class needs two fields and a constructor with two parameters. The driver below already calls new Book(title, pages).", "class Book { String title; int pages; Book(String title, int pages) { this.title = title; this.pages = pages; } }"),
    starter_compiles=False, difficulty=2)
ex.method("write", "j2-l1.1-write-student", "Complete the constructor", ["o1", "o2"], ["J2.01"], ["IMPL"],
    "`Student` has fields and a constructor, but the constructor doesn't store anything yet. Finish it, so that `best(...)` returns the name of the student with the higher grade (the first student if they tie).",
    [("best", [("name1", "String"), ("grade1", "int"), ("name2", "String"), ("grade2", "int")], "String")],
    {"best": lambda n1, g1, n2, g2: n1 if g1 >= g2 else n2},
    [("best", ["Ada", 90, "Bo", 80]), ("best", ["Ada", 70, "Bo", 80]), ("best", ["Ada", 80, "Bo", 80])],
    [("best", ["X", 0, "Y", 0]), ("best", ["Mia", 100, "Leo", 99]), ("best", ["Mia", 99, "Leo", 100]), ("best", ["A", 51, "B", 50]), ("best", ["A", 49, "B", 50])],
    'class Student {\n    String name;\n    int grade;\n\n    Student(String name, int grade) {\n        // store the values here\n    }\n}\n\nString best(String name1, int grade1, String name2, int grade2) {\n    Student a = new Student(name1, grade1);\n    Student b = new Student(name2, grade2);\n    return a.grade >= b.grade ? a.name : b.name;\n}',
    'class Student {\n    String name;\n    int grade;\n\n    Student(String name, int grade) {\n        this.name = name;\n        this.grade = grade;\n    }\n}\n\nString best(String name1, int grade1, String name2, int grade2) {\n    Student a = new Student(name1, grade1);\n    Student b = new Student(name2, grade2);\n    return a.grade >= b.grade ? a.name : b.name;\n}',
    {"names-only": 'class Student {\n    String name;\n    int grade;\n    Student(String name, int grade) {\n        this.name = name;\n    }\n}\n\nString best(String name1, int grade1, String name2, int grade2) {\n    Student a = new Student(name1, grade1);\n    Student b = new Student(name2, grade2);\n    return a.grade >= b.grade ? a.name : b.name;\n}',
     "swapped-grades": 'class Student {\n    String name;\n    int grade;\n    Student(String name, int grade) {\n        this.name = name;\n        this.grade = -grade;\n    }\n}\n\nString best(String name1, int grade1, String name2, int grade2) {\n    Student a = new Student(name1, grade1);\n    Student b = new Student(name2, grade2);\n    return a.grade >= b.grade ? a.name : b.name;\n}'},
    ("Inside the constructor, use this.name and this.grade for the fields, and the plain names for the parameters.", "this.name = name; this.grade = grade;"),
    difficulty=2)
ex.method("debug", "j2-l1.1-debug-shadow", "The constructor that compiles but does nothing", ["o1"], ["J2.01"], ["DEBUG"],
    "`sumOf(3, 4)` should return `7`, but it returns `0`. Find the bug in `Point`, and fix it. Don't change `sumOf`.",
    [("sumOf", [("a", "int"), ("b", "int")], "int")],
    {"sumOf": lambda a, b: a + b},
    [("sumOf", [3, 4]), ("sumOf", [0, 0]), ("sumOf", [-2, 5])],
    [("sumOf", [10, 20]), ("sumOf", [-7, -3]), ("sumOf", [100, 0]), ("sumOf", [1, 1]), ("sumOf", [0, 9])],
    'class Point {\n    int x;\n    int y;\n\n    Point(int x, int y) {\n        x = x;\n        y = y;\n    }\n}\n\nint sumOf(int a, int b) {\n    Point p = new Point(a, b);\n    return p.x + p.y;\n}',
    'class Point {\n    int x;\n    int y;\n\n    Point(int x, int y) {\n        this.x = x;\n        this.y = y;\n    }\n}\n\nint sumOf(int a, int b) {\n    Point p = new Point(a, b);\n    return p.x + p.y;\n}',
    {"fixed-x-only": 'class Point {\n    int x;\n    int y;\n    Point(int x, int y) {\n        this.x = x;\n        y = y;\n    }\n}\n\nint sumOf(int a, int b) {\n    Point p = new Point(a, b);\n    return p.x + p.y;\n}'},
    ("In a constructor, which x is on each side of x = x? Is the field ever assigned?", "Write this.x = x; and this.y = y;"),
    difficulty=2)
ex.predict("j2-l1.1-predict-objects", "Each object has its own fields", ["o2"], ["J2.01"],
    "Work out exactly what this program prints, one line per `IO.println`. Think about which object each line looks at, and what a field holds if it was never set.",
    '''class Box {
    int size;
    String label;
    boolean open;

    Box(int size) {
        this.size = size;
    }
}

void main() {
    Box a = new Box(5);
    Box b = new Box(5);
    b.size = 9;
    IO.println(a.size);
    IO.println(b.size);
    IO.println(a.label);
    IO.println(a.open);
}''', "5\n9\nnull\nfalse",
    ("Are a and b the same object? What does the constructor set, and what is left alone?", "a and b are separate objects. The constructor only sets size, so label is null and open is false."),
    difficulty=2)
ex.explain("j2-l1.1-explain-class-object", "Class, object, constructor", ["o3"], ["J2.01"],
    "A friend says: \"I don't get what the difference is between a class and an object, and why I need a constructor.\" Using a `Student` class with a `name` and a `grade` as your example, explain (a) what the class is, (b) what an object is and how you make one, and (c) what the constructor does and what goes wrong without one.",
    "A full answer says the class is the blueprint describing the fields every student has; an object is one actual student made with new, with its own values; and the constructor runs when you write new and sets the fields so the object starts in a usable state (without it, fields hold defaults such as null and 0 until you set each by hand).",
    {2: ("Explains the class as the description and the object as one instance made with new with its own field values, and says the constructor sets up the fields when new runs, with the default values as the alternative.",
         ["The Student class describes what every student has: a name and a grade. An object is one particular student, made with new Student(\"Ada\", 90), and it has its own name and grade. The constructor runs when new is called and sets those fields, so without it the fields would just be null and 0 until I set each one myself.",
          "A class is a blueprint and an object is a thing built from it. I can build many students from one class and each keeps its own values. The constructor is the code that fills in the name and grade at the moment of new, so the student is ready to use straight away."]),
     1: ("Explains one or two of the three ideas correctly, but confuses class and object or doesn't say what the constructor does.",
         ["A class is like an object.", "The constructor makes the object."]),
     0: ("Incorrect, for example says an object is a kind of variable type or that a constructor deletes the object.",
         ["An object is the blueprint.", "A constructor ends the program."])})

reg({"j2-l1.1": ("From main to a class", ["J2.01"])},
    {"MC27": (["J2.01"], "R8", "A class and an object are the same thing (Student.name instead of s.name)"),
     "MC28": (["J2.01"], "Platform", "name = name; in a constructor sets the field"),
     "MC29": (["J2.01"], "R8", "An object field of type String starts as an empty string")})

# ====================================================================== 2.1.2
Lesson("j2-l1.2", "Methods and this", ["J2.02"], [
    ("o1", "Write instance methods that read and change an object's fields"),
    ("o2", "Say which object a method call acts on, and what this means inside a method"),
    ("o3", "Change an existing method of a class to add a rule, without breaking its callers"),
], ["j2-l1.1"], 40, ["R8", "R5"], r'''
## Before you start

You should be able to write a class with fields and a constructor ([From main to a class](j2-l1.1)).

**Quick check.** Given `Student a = new Student("Ada", 90);` and `Student b = new Student("Bo", 70);`, what is `a.grade`? What is `b.grade`?

<details><summary>Show the answer</summary>

`90` and `70`. Each object has its own fields.

</details>

## Explanation

Fields hold what an object **knows**. **Methods** say what an object can **do**. Putting both in one class is the heart of object-oriented programming: the data and the code that works on it travel together.

### Instance methods

A method written inside a class, without `static`, is an **instance method**. It's called *on* an object, with a dot:

```java runnable
class Counter {
    int count;

    void increment() {
        count++;
    }

    int value() {
        return count;
    }
}

void main() {
    Counter c = new Counter();
    c.increment();
    c.increment();
    IO.println(c.value());
}
```

This prints `2`. Notice that `increment` takes no parameters, yet it knows which counter to change. The object before the dot is the one the method works on.

### `this`: the object the method was called on

Inside an instance method, the name `count` means *the `count` field of the object the method was called on*. You can write that out in full as `this.count`:

```java
void increment() {
    this.count++;      // identical to count++
}
```

`this` is a reference to the current object. You normally leave it out when there's no confusion, and you need it when a parameter or local variable has the same name as a field:

```java
void setCount(int count) {
    this.count = count;     // field = parameter
}
```

### Two objects, one class, separate state

```java
Counter a = new Counter();
Counter b = new Counter();
a.increment();
a.increment();
b.increment();
// a.value() is 2, b.value() is 1
```

The code of `increment` exists once, but each call works on whichever object is in front of the dot. That's why `a.increment()` and `b.increment()` change different fields.

### Methods that return `this`

A method can hand back the object it worked on, which lets you chain calls:

```java
Counter inc() {
    count++;
    return this;
}
// c.inc().inc().inc();    // three increments in one line
```

### Methods can use other methods and take parameters

An instance method can call the object's other methods by name (they're called on `this` automatically), take parameters and return values, just like the methods you already know:

```java
void add(int amount) {
    count += amount;
}
```

### Changing a method safely

When you change a method that other code already calls, keep its **name, parameters and return type** the same unless you also fix every caller. Adding a rule inside the method is usually safe. Changing what its signature looks like usually isn't.

## Worked examples

### Example 1: a bank account with a rule

*Task: an `Account` should allow deposits, and withdrawals only when the money is there. A withdrawal should report whether it worked.*

**Step 1 — Fields:** `int balance` (in pence, so whole numbers).

**Step 2 — Methods:** `deposit(int amount)`, `boolean withdraw(int amount)`, `int balance()`.

**Step 3 — The rule goes inside `withdraw`:** check first, change only if allowed.

```java runnable
class Account {
    int balance;

    void deposit(int amount) {
        balance += amount;
    }

    boolean withdraw(int amount) {
        if (amount > balance) {
            return false;
        }
        balance -= amount;
        return true;
    }
}

void main() {
    Account a = new Account();
    a.deposit(500);
    IO.println(a.withdraw(200));
    IO.println(a.withdraw(900));
    IO.println(a.balance);
}
```

**Step 4 — Check.** It prints `true`, `false`, `300`: the second withdrawal was refused and the balance wasn't touched.

### Example 2: which object changes?

*Task: what does this print?*

```java
Counter x = new Counter();
Counter y = new Counter();
x.increment();
y.increment();
y.increment();
IO.println(x.value() + " " + y.value());
```

**Step 1 — Trace each call by the object before the dot.** `x.increment()` changes `x.count`; the two `y.increment()` calls change `y.count`.

**Step 2 — Read the values.** `x.count` is 1 and `y.count` is 2, so it prints `1 2`.

## Predict, then run

::exercise{id=j2-l1.2-predict-two-counters}

## Where this is used

- **Everything with behaviour:** an `Account` deposits and withdraws, a `Cart` adds and removes items, a `Player` moves and takes damage.
- **Frameworks** call methods on your objects without you writing the call, so the idea of "a method working on one particular object" shows up everywhere.
- **Fluent APIs** that chain calls (`builder.name("x").size(3)`) rely on methods returning `this`.

## Common mistakes

:::mistake{id=MC30}
**Thinking the method has its own copy of the fields.** There's only one `count` per object. Two calls on the same object change the same field.
:::

:::mistake{id=MC31}
**Thinking a method called on `a` can change `b`.** A call changes the object before the dot (and anything else it's explicitly given). Another object isn't touched.
:::

## Practice

::exercise{id=j2-l1.2-write-counter}

::exercise{id=j2-l1.2-modify-account}

::exercise{id=j2-l1.2-explain-this}

## Further reading

- **"A multi-national study of reading and tracing skills in novice programmers"** (Lister et al., 2004) `[R5]` found that weaker tracing is linked with weaker code writing, which is why this lesson asks you to trace calls on several objects.
- **Qian & Lehman (2017)** `[R8]` reviews research on novices' misunderstandings of methods and objects.

## How you'll be assessed

- The **write** exercise checks that you can write instance methods that read and change fields (*implementation*).
- The **predict** exercise checks that you can tell which object each call changes (*identifying mistakes*).
- The **modify** exercise checks that you can add a rule to an existing method (*modification*).
- The **explain** exercise checks that you can say what `this` is and why a method knows which object to use (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j2-l1.2")
def counter_run(ops):
    n = 0
    for op in ops:
        if op == "inc": n += 1
        elif op == "reset": n = 0
        elif op.startswith("add:"): n += int(op[4:])
    return n
ex.method("write", "j2-l1.2-write-counter", "A counter with behaviour", ["o1"], ["J2.02"], ["IMPL"],
    "Finish `Counter`. It needs `increment()` (adds 1), `add(int amount)`, `reset()` (back to 0) and `value()` (returns the current count). The driver `run` applies a list of operations such as `\"inc\"`, `\"add:5\"` and `\"reset\"`, and returns the final value.",
    [("run", [("ops", "String[]")], "int")], {"run": counter_run},
    [("run", [["inc", "inc", "add:5"]]), ("run", [["add:10", "reset", "inc"]]), ("run", [[]])],
    [("run", [["reset"]]), ("run", [["add:3", "add:4", "add:5"]]), ("run", [["inc", "reset", "reset", "inc", "inc"]]), ("run", [["add:-2", "inc"]]), ("run", [["add:100", "add:1"]])],
    'class Counter {\n    int count;\n\n    void increment() {\n    }\n\n    void add(int amount) {\n    }\n\n    void reset() {\n    }\n\n    int value() {\n        return 0;\n    }\n}\n\nint run(String[] ops) {\n    Counter c = new Counter();\n    for (String op : ops) {\n        if (op.equals("inc")) {\n            c.increment();\n        } else if (op.equals("reset")) {\n            c.reset();\n        } else if (op.startsWith("add:")) {\n            c.add(Integer.parseInt(op.substring(4)));\n        }\n    }\n    return c.value();\n}',
    'class Counter {\n    int count;\n\n    void increment() {\n        count++;\n    }\n\n    void add(int amount) {\n        count += amount;\n    }\n\n    void reset() {\n        count = 0;\n    }\n\n    int value() {\n        return count;\n    }\n}\n\nint run(String[] ops) {\n    Counter c = new Counter();\n    for (String op : ops) {\n        if (op.equals("inc")) {\n            c.increment();\n        } else if (op.equals("reset")) {\n            c.reset();\n        } else if (op.startsWith("add:")) {\n            c.add(Integer.parseInt(op.substring(4)));\n        }\n    }\n    return c.value();\n}',
    {"reset-does-nothing": 'class Counter {\n    int count;\n    void increment() { count++; }\n    void add(int amount) { count += amount; }\n    void reset() { }\n    int value() { return count; }\n}\n\nint run(String[] ops) {\n    Counter c = new Counter();\n    for (String op : ops) {\n        if (op.equals("inc")) c.increment();\n        else if (op.equals("reset")) c.reset();\n        else if (op.startsWith("add:")) c.add(Integer.parseInt(op.substring(4)));\n    }\n    return c.value();\n}',
     "add-replaces": 'class Counter {\n    int count;\n    void increment() { count++; }\n    void add(int amount) { count = amount; }\n    void reset() { count = 0; }\n    int value() { return count; }\n}\n\nint run(String[] ops) {\n    Counter c = new Counter();\n    for (String op : ops) {\n        if (op.equals("inc")) c.increment();\n        else if (op.equals("reset")) c.reset();\n        else if (op.startsWith("add:")) c.add(Integer.parseInt(op.substring(4)));\n    }\n    return c.value();\n}'},
    ("Each method works on the count field of the object it's called on. Fill in the four bodies.", "increment: count++; add: count += amount; reset: count = 0; value: return count;"),
    difficulty=2)
def account_run(start, amounts):
    bal, ok = start, 0
    for a in amounts:
        if a >= 0: bal += a
        else:
            if -a <= bal: bal -= -a; ok += 1
    return f"{bal},{ok}"
ex.method("modify", "j2-l1.2-modify-account", "Refuse an overdraft", ["o3"], ["J2.02"], ["MOD"],
    "`Account.withdraw` currently lets the balance go negative and always reports success. Change it so that a withdrawal bigger than the balance is **refused**: the balance is left alone and `withdraw` returns `false`. A successful withdrawal returns `true`. Don't change the method's name or parameters, because `run` already calls it.",
    [("run", [("start", "int"), ("amounts", "int[]")], "String")], {"run": account_run},
    [("run", [100, [50, -30, -200]]), ("run", [0, [-1]]), ("run", [500, []])],
    [("run", [100, [-100]]), ("run", [100, [-101]]), ("run", [10, [-5, -5, -5]]), ("run", [0, [20, -20, -1]]), ("run", [1000, [-400, -400, -400, 50]])],
    'class Account {\n    int balance;\n\n    Account(int balance) {\n        this.balance = balance;\n    }\n\n    void deposit(int amount) {\n        balance += amount;\n    }\n\n    boolean withdraw(int amount) {\n        balance -= amount;\n        return true;\n    }\n}\n\nString run(int start, int[] amounts) {\n    Account acct = new Account(start);\n    int ok = 0;\n    for (int a : amounts) {\n        if (a >= 0) {\n            acct.deposit(a);\n        } else if (acct.withdraw(-a)) {\n            ok++;\n        }\n    }\n    return acct.balance + "," + ok;\n}',
    'class Account {\n    int balance;\n\n    Account(int balance) {\n        this.balance = balance;\n    }\n\n    void deposit(int amount) {\n        balance += amount;\n    }\n\n    boolean withdraw(int amount) {\n        if (amount > balance) {\n            return false;\n        }\n        balance -= amount;\n        return true;\n    }\n}\n\nString run(int start, int[] amounts) {\n    Account acct = new Account(start);\n    int ok = 0;\n    for (int a : amounts) {\n        if (a >= 0) {\n            acct.deposit(a);\n        } else if (acct.withdraw(-a)) {\n            ok++;\n        }\n    }\n    return acct.balance + "," + ok;\n}',
    {"refuses-at-equal": 'class Account {\n    int balance;\n    Account(int balance) { this.balance = balance; }\n    void deposit(int amount) { balance += amount; }\n    boolean withdraw(int amount) {\n        if (amount >= balance) return false;\n        balance -= amount;\n        return true;\n    }\n}\n\nString run(int start, int[] amounts) {\n    Account acct = new Account(start);\n    int ok = 0;\n    for (int a : amounts) {\n        if (a >= 0) acct.deposit(a);\n        else if (acct.withdraw(-a)) ok++;\n    }\n    return acct.balance + "," + ok;\n}',
     "refuses-but-says-true": 'class Account {\n    int balance;\n    Account(int balance) { this.balance = balance; }\n    void deposit(int amount) { balance += amount; }\n    boolean withdraw(int amount) {\n        if (amount <= balance) balance -= amount;\n        return true;\n    }\n}\n\nString run(int start, int[] amounts) {\n    Account acct = new Account(start);\n    int ok = 0;\n    for (int a : amounts) {\n        if (a >= 0) acct.deposit(a);\n        else if (acct.withdraw(-a)) ok++;\n    }\n    return acct.balance + "," + ok;\n}'},
    ("Check the rule before changing the balance. What should happen to the balance when the withdrawal is refused?", "if (amount > balance) { return false; } balance -= amount; return true;"),
    difficulty=2)
ex.predict("j2-l1.2-predict-two-counters", "Which counter changes?", ["o2"], ["J2.02"],
    "Work out what this program prints. Be careful about which object each call is made on, and what the chained calls return.",
    '''class Counter {
    int n;

    Counter inc() {
        n++;
        return this;
    }

    int value() {
        return n;
    }
}

void main() {
    Counter a = new Counter();
    Counter b = new Counter();
    a.inc().inc().inc();
    b.inc().inc();
    a.inc();
    IO.println(a.value() + " " + b.value());
}''', "4 2",
    ("Count the inc() calls made on a, and on b, separately.", "a gets three increments in the chain and one more later, so 4. b gets two, so 2."),
    difficulty=2)
ex.explain("j2-l1.2-explain-this", "How does the method know which object?", ["o2"], ["J2.02"],
    "A learner writes `Counter a = new Counter(); Counter b = new Counter(); a.increment(); b.increment(); b.increment();` and asks: \"`increment()` has no parameters. How does it know to change `a`'s count the first time and `b`'s the other times, and what is `this`?\" Answer them, and say what `a.count` and `b.count` are afterwards.",
    "A full answer says a method call acts on the object before the dot, which becomes this inside the method; so count means this.count of that object; after the calls a.count is 1 and b.count is 2.",
    {2: ("Says the object before the dot is the one the method works on, and inside the method this refers to that object so count means this.count; and gives a.count = 1 and b.count = 2.",
         ["The method works on the object you call it on, the one before the dot. Inside the method, this means that object, and plain count is short for this.count. So a.increment() changes a's count and b.increment() changes b's. After the three calls a.count is 1 and b.count is 2.",
          "When you write a.increment(), Java passes a along invisibly as this. So count++ really means this.count++ on a. For b it's b. That gives a.count = 1 and b.count = 2."]),
     1: ("Gets part of it, for example says the object before the dot is used, but not what this is, or gets one of the final counts wrong.",
         ["It changes the one you call it on.", "a is 1 and b is 1."]),
     0: ("Incorrect, for example says the method has one shared count for all counters or that this is a parameter you pass.",
         ["There's one count shared by everything.", "this is the number you pass in."])})

reg({"j2-l1.2": ("Methods and this", ["J2.02"])},
    {"MC30": (["J2.02"], "R8", "Each method call gets its own copy of the object's fields"),
     "MC31": (["J2.02"], "R8", "A method called on one object can change a different object of the same class")})

# ====================================================================== 2.1.3
Lesson("j2-l1.3", "Objects and references", ["J2.03"], [
    ("o1", "Explain that an object variable holds a reference, and that assigning it copies the reference and not the object"),
    ("o2", "Predict the result of code with aliases, == and equals on objects"),
    ("o3", "Fix bugs caused by aliasing and by null references"),
], ["j2-l1.2", "j1-l6.2"], 45, ["R8", "R18"], r'''
## Before you start

You've seen that two array variables can refer to the same array ([Array algorithms and references](j1-l6.2)). Objects work the same way.

**Quick check.** After `int[] a = {1, 2}; int[] b = a; b[0] = 9;`, what is `a[0]`?

<details><summary>Show the answer</summary>

`9`. `a` and `b` are two names for **one** array.

</details>

## Explanation

### A variable holds a reference, not the object

```java
Player a = new Player("Sam");
```

`new Player("Sam")` builds an object in memory. The variable `a` holds a **reference** to it, something like the address of where it lives. Picture it as an arrow:

```
a ──▶ [ Player: name "Sam", score 0 ]
```

### Copying a reference does not copy the object

```java
Player b = a;
```

`b` receives a copy of the **arrow**, not a copy of the player:

```
a ──▶ [ Player: name "Sam", score 0 ]
b ──▶ (the same one)
```

Now `a` and `b` are **aliases**: two names for one object. Anything done through one is visible through the other:

```java runnable
class Player {
    String name;
    int score;

    Player(String name) {
        this.name = name;
    }
}

void main() {
    Player a = new Player("Sam");
    Player b = a;
    b.score = 50;
    IO.println(a.score);
}
```

This prints `50`. You changed the object through `b`, and `a` points at it too. Python Tutor, the step-through visualiser linked from lesson 2.2, draws exactly these arrows if you want to see them.

### Making a real copy

If you want a separate object, construct one:

```java
Player c = new Player(a.name);
c.score = a.score;
```

Now `c` is its own object with the same values. Changing `c` doesn't touch `a`.

### `==` compares references, `equals` compares meaning

For objects, `==` asks *are these two the very same object?* (same arrow target). It doesn't look inside:

```java
Player x = new Player("Sam");
Player y = new Player("Sam");
x == y        // false: two different objects, even with identical contents
x == x        // true
```

`equals` is a method meant to ask *do these count as equal?* For a class you write, `equals` starts out doing the same as `==`: it only says `true` for the very same object. The next lesson shows how to give it a meaning. For `String`, `equals` already compares the characters, which is why you use `.equals` and not `==` for text.

### `null`: a reference to nothing

A reference variable can hold `null`, meaning *no object*. Calling a method or reading a field through `null` crashes:

```java
Player p = null;
p.score;          // NullPointerException
```

Fields of object types start as `null`, which is where most of these crashes come from. Before using a reference that might be `null`, check: `if (p != null) { ... }`.

### Passing objects to methods

When you pass an object to a method, the method gets a copy of the **reference**. So it can change the object's fields, and the caller sees that. But assigning a different object to the parameter inside the method only changes the method's own copy of the arrow.

## Worked examples

### Example 1: spotting an alias

*Task: the code should record a player's score before a bonus and after it. What's wrong?*

```java
Player before = player;
player.score += 10;
IO.println(before.score + " -> " + player.score);
```

**Step 1 — What is `before`?** An alias of `player`, so the same object.

**Step 2 — So `player.score += 10` changes what `before` sees too.** It prints the new score twice.

**Step 3 — Fix: take a real copy before changing.**

```java
Player before = new Player(player.name);
before.score = player.score;
player.score += 10;
```

**Step 4 — Check.** `before` is its own object, so it keeps the old score.

### Example 2: a null crash

*Task: `team.captain.name` crashes when no captain was set. Make it safe.*

**Step 1 — Why does it crash?** The `captain` field is `null` until someone assigns it, and `.name` on `null` throws.

**Step 2 — Decide what should happen:** the answer is `"none"` when there's no captain.

**Step 3 — Check before using.**

```java
String captainName(Team team) {
    if (team.captain == null) {
        return "none";
    }
    return team.captain.name;
}
```

## Predict, then run

::exercise{id=j2-l1.3-predict-alias}

::exercise{id=j2-l1.3-predict-equality}

## Where this is used

- **Shared state bugs:** two parts of a program holding the same object and surprising each other is among the most common real bugs.
- **`NullPointerException`** is the most familiar Java exception. Reading code with "might this be null?" in mind is a daily habit.
- **Caching, collections and frameworks** all store references, so you need to know what is shared and what is copied.

## Common mistakes

:::mistake{id=MC32}
**Thinking `b = a` copies the object.** It copies the reference. Both variables now point at one object, so a change through either is seen through both.
:::

:::mistake{id=MC33}
**Using `==` to compare objects' contents.** `==` asks whether two references point at the same object. Two separate objects with identical fields are not `==`.
:::

:::mistake{id=MC34}
**Forgetting that object fields start as `null`.** Using such a field before assigning it throws `NullPointerException`.
:::

## Practice

::exercise{id=j2-l1.3-debug-copy}

::exercise{id=j2-l1.3-debug-null}

::exercise{id=j2-l1.3-explain-references}

## Further reading

- **Qian & Lehman (2017)** `[R8]` discuss how novices misread assignment of objects as copying them.
- **Guo (2013)** `[R18]` describes Python Tutor, the kind of step-through tool that draws these reference arrows.

## How you'll be assessed

- The **predict** exercises check that you can follow aliases and tell `==` from `equals` (*identifying mistakes*).
- The **debug** exercises check that you can fix a copy that was only an alias, and a null crash (*debugging*).
- The **explain** exercise checks that you can describe what a reference is and why two objects with equal contents aren't `==` (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''')

ex = Exercises("j2-l1.3")
ex.predict("j2-l1.3-predict-alias", "Two names, one object", ["o1", "o2"], ["J2.03"],
    "Work out what this program prints. Draw the references if it helps.",
    '''class Player {
    String name;
    int score;

    Player(String name) {
        this.name = name;
    }
}

void main() {
    Player a = new Player("Sam");
    Player b = a;
    b.score = 50;
    Player c = new Player("Sam");
    IO.println(a.score);
    IO.println(c.score);
    IO.println(a == b);
    IO.println(a == c);
}''', "50\n0\ntrue\nfalse",
    ("Which variables refer to the same object? c was built separately.", "a and b are one object. c is a new object, with score 0."),
    difficulty=2)
ex.predict("j2-l1.3-predict-equality", "equals before you've written one", ["o2"], ["J2.03"],
    "`Point` doesn't define `equals` yet. Work out what this prints.",
    '''class Point {
    int x;
    int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
}

void main() {
    Point p = new Point(1, 2);
    Point q = new Point(1, 2);
    Point r = p;
    IO.println(p == q);
    IO.println(p.equals(q));
    IO.println(p.equals(r));
    IO.println(p.x == q.x);
}''', "false\nfalse\ntrue\ntrue",
    ("A class that hasn't defined equals only treats the very same object as equal. What does p.x == q.x compare?", "p and q are different objects, so == and the default equals are false. r is p. p.x == q.x compares two ints."),
    difficulty=2)
ex.method("debug", "j2-l1.3-debug-copy", "The snapshot that isn't", ["o3"], ["J2.03"], ["DEBUG"],
    "`bonusTotals(score)` should return the score **before** and **after** a 10-point bonus, as an array of two numbers. It returns the new score twice. Fix `bonusTotals` (not `Player`) so that `before` really is the old state.",
    [("bonusTotals", [("score", "int")], "int[]")],
    {"bonusTotals": lambda s: [s, s + 10]},
    [("bonusTotals", [50]), ("bonusTotals", [0]), ("bonusTotals", [-5])],
    [("bonusTotals", [100]), ("bonusTotals", [7]), ("bonusTotals", [1]), ("bonusTotals", [999]), ("bonusTotals", [-10])],
    'class Player {\n    String name;\n    int score;\n\n    Player(String name, int score) {\n        this.name = name;\n        this.score = score;\n    }\n}\n\nint[] bonusTotals(int score) {\n    Player player = new Player("Sam", score);\n    Player before = player;\n    player.score += 10;\n    return new int[] {before.score, player.score};\n}',
    'class Player {\n    String name;\n    int score;\n\n    Player(String name, int score) {\n        this.name = name;\n        this.score = score;\n    }\n}\n\nint[] bonusTotals(int score) {\n    Player player = new Player("Sam", score);\n    Player before = new Player(player.name, player.score);\n    player.score += 10;\n    return new int[] {before.score, player.score};\n}',
    {"copies-after-change": 'class Player {\n    String name;\n    int score;\n    Player(String name, int score) { this.name = name; this.score = score; }\n}\n\nint[] bonusTotals(int score) {\n    Player player = new Player("Sam", score);\n    player.score += 10;\n    Player before = new Player(player.name, player.score);\n    return new int[] {before.score, player.score};\n}'},
    ("What does Player before = player; give you: a second player, or a second name for the first?", "Create a real copy with new Player(...) before the bonus is added."),
    difficulty=3)
ex.method("debug", "j2-l1.3-debug-null", "The captain who isn't there", ["o3"], ["J2.03"], ["DEBUG"],
    "`captainName(name, hasCaptain)` should return the captain's name, or `\"none\"` if the team has no captain. It crashes with a `NullPointerException` when there's no captain. Fix it.",
    [("captainName", [("name", "String"), ("hasCaptain", "boolean")], "String")],
    {"captainName": lambda n, h: n if h else "none"},
    [("captainName", ["Ada", True]), ("captainName", ["Ada", False]), ("captainName", ["", True])],
    [("captainName", ["Bo", True]), ("captainName", ["Bo", False]), ("captainName", ["none", True]), ("captainName", ["Zed", False]), ("captainName", ["X", True])],
    'class Player {\n    String name;\n\n    Player(String name) {\n        this.name = name;\n    }\n}\n\nclass Team {\n    Player captain;\n}\n\nString captainName(String name, boolean hasCaptain) {\n    Team team = new Team();\n    if (hasCaptain) {\n        team.captain = new Player(name);\n    }\n    return team.captain.name;\n}',
    'class Player {\n    String name;\n\n    Player(String name) {\n        this.name = name;\n    }\n}\n\nclass Team {\n    Player captain;\n}\n\nString captainName(String name, boolean hasCaptain) {\n    Team team = new Team();\n    if (hasCaptain) {\n        team.captain = new Player(name);\n    }\n    if (team.captain == null) {\n        return "none";\n    }\n    return team.captain.name;\n}',
    {"always-none": 'class Player {\n    String name;\n    Player(String name) { this.name = name; }\n}\n\nclass Team {\n    Player captain;\n}\n\nString captainName(String name, boolean hasCaptain) {\n    return "none";\n}'},
    ("What is team.captain when hasCaptain is false?", "Check team.captain == null before reading .name, and return \"none\" in that case."),
    difficulty=2)
ex.explain("j2-l1.3-explain-references", "Two players with the same name", ["o1", "o2"], ["J2.03"],
    "Given `Player a = new Player(\"Sam\"); Player b = a; Player c = new Player(\"Sam\");`: (a) explain what is in the variables `a`, `b` and `c`, (b) say whether `a == b` and `a == c` are true and why, and (c) say what happens to `a.score` if you run `b.score = 50;`, and what happens to `c.score`.",
    "A full answer says each variable holds a reference; a and b hold references to the same object but c refers to a separate object; so a == b is true and a == c is false even though the names match; b.score = 50 changes the shared object so a.score is 50, and c.score is unchanged.",
    {2: ("Says variables hold references; a and b refer to the same object and c to a different one; a == b true, a == c false because == compares references; a.score becomes 50 and c.score is unchanged.",
         ["a, b and c each hold a reference. a and b refer to the same Player object, because b = a copied the reference, while c is a separate object that happens to have the same name. So a == b is true and a == c is false. Setting b.score = 50 changes that one shared object, so a.score is 50, but c is a different object and keeps its own score.",
          "The variables store arrows to objects, not the objects. a and b point to one object; c points to another. == checks if two arrows go to the same object, so a == b is true and a == c is false. b.score = 50 also changes a.score, and c.score stays as it was."]),
     1: ("Correct on one or two of the parts, for example gets a == b and a == c right but doesn't explain, or doesn't say what happens to c.",
         ["a == b is true and a == c is false.", "a.score becomes 50."]),
     0: ("Incorrect, for example says b is a copy of the object, or that a == c is true because the names match.",
         ["b is a copy, so a.score stays 0.", "a == c is true because both are Sam."])})

reg({"j2-l1.3": ("Objects and references", ["J2.03"])},
    {"MC32": (["J2.03"], "R8", "Player b = a; makes a separate copy of the object"),
     "MC33": (["J2.03"], "R8", "== on objects compares their contents"),
     "MC34": (["J2.03"], "Platform", "Object-typed fields start with a usable value, not null")})

# ====================================================================== 2.1.4
Lesson("j2-l1.4", "static, toString and equals", ["J2.04"], [
    ("o1", "Say what static means, and use static methods and constants"),
    ("o2", "Write a toString method so an object prints meaningfully"),
    ("o3", "Override equals and hashCode together, and say why they must agree"),
], ["j2-l1.3"], 45, ["R8", "I38"], r'''
## Before you start

You should know that `==` on objects compares references, and that a class you write starts with an `equals` that does the same ([Objects and references](j2-l1.3)).

**Quick check.** What does `new Point(1, 2).equals(new Point(1, 2))` return, if `Point` hasn't defined `equals`?

<details><summary>Show the answer</summary>

`false`. The default `equals` only says `true` for the very same object.

</details>

## Explanation

### `static`: belongs to the class, not to an object

An instance method or field belongs to **each object**: `c.increment()`, `s.name`. A **`static`** member belongs to **the class itself**, and you reach it through the class name:

```java
class Temperature {
    static final double FREEZING = 0.0;

    static double toFahrenheit(double celsius) {
        return celsius * 9 / 5 + 32;
    }
}
// Temperature.toFahrenheit(100)   // 212.0
// Temperature.FREEZING            // 0.0
```

Use `static` for:

- **Constants** (`static final`): a value that never changes and is shared, such as a tax rate or a limit.
- **Helper methods that need no object's data**: they take everything they need as parameters. `Math.max` and `Integer.parseInt` are static.

A static method can't use `this` or any instance field, because it isn't called on an object.

### Shared state: use with care

A non-final `static` field is **one variable shared by every object** of the class, and by the whole program. It's easy to misuse, because any code anywhere can change it, so bugs become hard to trace. Prefer instance fields. Use static for constants and pure helpers.

### `toString`: how an object describes itself

Every object has a `toString()` method, and Java calls it whenever an object is turned into text, such as in `"P=" + p` or `IO.println(p)`. If you don't write one, you get the class name, an `@`, and a hash code, something like `Point@1b6d3586` `[I38]`, which is no use to anyone. Write your own:

```java
class Point {
    int x;
    int y;
    Point(int x, int y) { this.x = x; this.y = y; }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}
// IO.println(new Point(3, 4));   // (3, 4)
```

`@Override` asks the compiler to check that you really are replacing an inherited method; it catches typos. `toString` must be `public`, because it replaces a public method.

### `equals`: when two objects count as the same

For a `Point`, you probably want two points with the same coordinates to be equal. Override `equals`:

```java
@Override
public boolean equals(Object other) {
    if (this == other) return true;
    if (!(other instanceof Point p)) return false;
    return x == p.x && y == p.y;
}
```

- The parameter is an `Object`, so any object can be passed in. Use `instanceof` to check it's a `Point`, and the pattern `Point p` gives you a typed variable in one step.
- A correct `equals` is reflexive, symmetric and transitive `[I38]`: `a.equals(a)` is true, `a.equals(b)` agrees with `b.equals(a)`, and equality chains.

### `hashCode`: the partner of `equals`

Collections such as `HashMap` and `HashSet` use an object's `hashCode()` to decide where to look for it (you'll meet them in Stage 3). The rule from the Java documentation is: **if two objects are equal according to `equals`, they must return the same `hashCode`**, though unequal objects may share one `[I38]`. So whenever you override `equals`, override `hashCode` too:

```java
@Override
public int hashCode() {
    return Objects.hash(x, y);
}
```

`Objects.hash` combines the values for you. Forgetting `hashCode` is a classic bug: two equal objects can go to different places in a hash-based collection, so a lookup misses an object that's really there.

## Worked examples

### Example 1: making a point printable

*Task: `IO.println(new Point(3, 4))` shows `Point@6d06d69c`. Make it show `(3, 4)`.*

**Step 1 — Where does that text come from?** The default `toString` `[I38]`.

**Step 2 — Override it** in `Point`, `public String toString()`, building the text from the fields.

**Step 3 — Check.** The output is now `(3, 4)`, and so is `"P=" + p`, which gives `P=(3, 4)`.

### Example 2: equals and hashCode together

*Task: two points with the same x and y should be equal.*

**Step 1 — Decide what "same" means:** equal `x` and equal `y`.

**Step 2 — Write `equals`** comparing those fields, with the `instanceof` check.

**Step 3 — Write `hashCode`** from the same fields.

```java runnable
class Point {
    int x;
    int y;
    Point(int x, int y) { this.x = x; this.y = y; }

    @Override
    public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof Point p)) return false;
        return x == p.x && y == p.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}

void main() {
    Point a = new Point(1, 2);
    Point b = new Point(1, 2);
    IO.println(a.equals(b));
    IO.println(a.hashCode() == b.hashCode());
}
```

**Step 4 — Check.** Both lines print `true`.

## Where this is used

- **Logs and debugging:** a useful `toString` turns `Account@4f23` into `Account[id=7, balance=500]`, and saves hours.
- **Collections:** sets, map keys and `contains` checks all rely on `equals` and `hashCode`.
- **Constants:** `static final` values like `MAX_RETRIES` keep magic numbers out of your code.

## Common mistakes

:::mistake{id=MC35}
**Overriding `equals` but not `hashCode`.** Equal objects must have equal hash codes. If they don't, hash-based collections can fail to find an object that's there.
:::

:::mistake{id=MC36}
**Using a mutable `static` field to hold per-object data.** There's only one copy, shared by everything. Use an instance field.
:::

:::mistake{id=MC37}
**Writing `equals(Point other)` instead of `equals(Object other)`.** That's a different method, so the one collections call is still the default. `@Override` makes the compiler catch this.
:::

## Practice

::exercise{id=j2-l1.4-write-tostring}

::exercise{id=j2-l1.4-write-equals}

::exercise{id=j2-l1.4-modify-static}

::exercise{id=j2-l1.4-explain-equals-hash}

## Version notes

`instanceof` with a pattern variable (`other instanceof Point p`) arrived in **Java 16**. Older code writes the cast separately: `if (!(other instanceof Point)) return false; Point p = (Point) other;`. Records (lesson 2.4.1) write `equals`, `hashCode` and `toString` for you.

## Further reading

- **The `java.lang.Object` documentation** `[I38]` states the `equals` and `hashCode` contract in full.
- **Qian & Lehman (2017)** `[R8]` covers novice confusion between class-level and object-level members.

## How you'll be assessed

- The **write** exercises check that you can write `toString`, `equals` and `hashCode` (*implementation*).
- The **modify** exercise checks that you can turn an instance helper into a `static` method with a constant (*modification*).
- The **explain** exercise checks that you can say why `equals` and `hashCode` must agree (*explanation*).

An exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.
''', features=[("instanceof patterns", 16)])

ex = Exercises("j2-l1.4")
ex.method("write", "j2-l1.4-write-tostring", "Make a point printable", ["o2"], ["J2.04"], ["IMPL"],
    "Write `toString` for `Point` so that a point at x=3, y=4 appears as `(3, 4)`. The driver `show` wraps it as `P=(3, 4)`. Remember `toString` must be `public`.",
    [("show", [("x", "int"), ("y", "int")], "String")],
    {"show": lambda x, y: f"P=({x}, {y})"},
    [("show", [3, 4]), ("show", [0, 0]), ("show", [-1, 5])],
    [("show", [10, 20]), ("show", [-7, -8]), ("show", [100, 0]), ("show", [1, 1]), ("show", [0, -9])],
    'class Point {\n    int x;\n    int y;\n\n    Point(int x, int y) {\n        this.x = x;\n        this.y = y;\n    }\n\n    // write toString here\n}\n\nString show(int x, int y) {\n    Point p = new Point(x, y);\n    return "P=" + p;\n}',
    'class Point {\n    int x;\n    int y;\n\n    Point(int x, int y) {\n        this.x = x;\n        this.y = y;\n    }\n\n    @Override\n    public String toString() {\n        return "(" + x + ", " + y + ")";\n    }\n}\n\nString show(int x, int y) {\n    Point p = new Point(x, y);\n    return "P=" + p;\n}',
    {"no-space": 'class Point {\n    int x;\n    int y;\n    Point(int x, int y) { this.x = x; this.y = y; }\n    @Override\n    public String toString() { return "(" + x + "," + y + ")"; }\n}\n\nString show(int x, int y) {\n    Point p = new Point(x, y);\n    return "P=" + p;\n}',
     "x-twice": 'class Point {\n    int x;\n    int y;\n    Point(int x, int y) { this.x = x; this.y = y; }\n    @Override\n    public String toString() { return "(" + x + ", " + x + ")"; }\n}\n\nString show(int x, int y) {\n    Point p = new Point(x, y);\n    return "P=" + p;\n}'},
    ("Write public String toString() and build the text from the fields, with the brackets and the comma and space.", "return \"(\" + x + \", \" + y + \")\";"),
    difficulty=2)
ex.method("write", "j2-l1.4-write-equals", "Equal points", ["o3"], ["J2.04"], ["IMPL"],
    "Write `equals` and `hashCode` for `Point` so that two points with the same `x` and `y` are equal, and equal points have the same hash code. `compare` reports whether the points are equal, and then whether the hash-code rule holds (equal objects must give equal hash codes), as `true,true` for example.",
    [("compare", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "String")],
    {"compare": lambda x1, y1, x2, y2: f"{str(x1 == x2 and y1 == y2).lower()},true"},
    [("compare", [1, 2, 1, 2]), ("compare", [1, 2, 3, 4]), ("compare", [0, 0, 0, 0])],
    [("compare", [1, 2, 2, 1]), ("compare", [5, 5, 5, 6]), ("compare", [-1, -1, -1, -1]), ("compare", [7, 8, 8, 8]), ("compare", [100, 200, 100, 200])],
    'class Point {\n    int x;\n    int y;\n\n    Point(int x, int y) {\n        this.x = x;\n        this.y = y;\n    }\n\n    // write equals and hashCode here\n}\n\nString compare(int x1, int y1, int x2, int y2) {\n    Point a = new Point(x1, y1);\n    Point b = new Point(x2, y2);\n    boolean equal = a.equals(b);\n    boolean hashRule = !equal || a.hashCode() == b.hashCode();\n    return equal + "," + hashRule;\n}',
    'class Point {\n    int x;\n    int y;\n\n    Point(int x, int y) {\n        this.x = x;\n        this.y = y;\n    }\n\n    @Override\n    public boolean equals(Object other) {\n        if (this == other) return true;\n        if (!(other instanceof Point p)) return false;\n        return x == p.x && y == p.y;\n    }\n\n    @Override\n    public int hashCode() {\n        return Objects.hash(x, y);\n    }\n}\n\nString compare(int x1, int y1, int x2, int y2) {\n    Point a = new Point(x1, y1);\n    Point b = new Point(x2, y2);\n    boolean equal = a.equals(b);\n    boolean hashRule = !equal || a.hashCode() == b.hashCode();\n    return equal + "," + hashRule;\n}',
    {"equals-without-hashcode": 'class Point {\n    int x;\n    int y;\n    Point(int x, int y) { this.x = x; this.y = y; }\n    @Override\n    public boolean equals(Object other) {\n        if (this == other) return true;\n        if (!(other instanceof Point p)) return false;\n        return x == p.x && y == p.y;\n    }\n}\n\nString compare(int x1, int y1, int x2, int y2) {\n    Point a = new Point(x1, y1);\n    Point b = new Point(x2, y2);\n    boolean equal = a.equals(b);\n    boolean hashRule = !equal || a.hashCode() == b.hashCode();\n    return equal + "," + hashRule;\n}',
     "compares-x-only": 'class Point {\n    int x;\n    int y;\n    Point(int x, int y) { this.x = x; this.y = y; }\n    @Override\n    public boolean equals(Object other) {\n        if (!(other instanceof Point p)) return false;\n        return x == p.x;\n    }\n    @Override\n    public int hashCode() { return Objects.hash(x); }\n}\n\nString compare(int x1, int y1, int x2, int y2) {\n    Point a = new Point(x1, y1);\n    Point b = new Point(x2, y2);\n    boolean equal = a.equals(b);\n    boolean hashRule = !equal || a.hashCode() == b.hashCode();\n    return equal + "," + hashRule;\n}'},
    ("equals takes an Object. Check it's a Point, then compare both fields. hashCode should use the same fields.", "return x == p.x && y == p.y;  and  return Objects.hash(x, y);"),
    difficulty=3)
ex.method("modify", "j2-l1.4-modify-static", "A tax helper that needs no object", ["o1"], ["J2.04"], ["MOD"],
    "`Shop.priceWithTax` doesn't use any field, so it shouldn't need a `Shop` object. The driver `total` calls it as `Shop.priceWithTax(pence)`, which doesn't compile yet. Make the method `static`, and replace the number `20` with a `static final int TAX_PERCENT = 20;` constant. It adds the tax and rounds down: `price * (100 + 20) / 100` in whole pence.",
    [("total", [("pence", "int")], "int")],
    {"total": lambda p: p * 120 // 100},
    [("total", [1000]), ("total", [0]), ("total", [99])],
    [("total", [1]), ("total", [5]), ("total", [12345]), ("total", [250]), ("total", [3])],
    'class Shop {\n    int priceWithTax(int pence) {\n        return pence * (100 + 20) / 100;\n    }\n}\n\nint total(int pence) {\n    return Shop.priceWithTax(pence);\n}',
    'class Shop {\n    static final int TAX_PERCENT = 20;\n\n    static int priceWithTax(int pence) {\n        return pence * (100 + TAX_PERCENT) / 100;\n    }\n}\n\nint total(int pence) {\n    return Shop.priceWithTax(pence);\n}',
    {"wrong-rate": 'class Shop {\n    static final int TAX_PERCENT = 10;\n    static int priceWithTax(int pence) {\n        return pence * (100 + TAX_PERCENT) / 100;\n    }\n}\n\nint total(int pence) {\n    return Shop.priceWithTax(pence);\n}',
     "rounds-up": 'class Shop {\n    static final int TAX_PERCENT = 20;\n    static int priceWithTax(int pence) {\n        return (pence * (100 + TAX_PERCENT) + 99) / 100;\n    }\n}\n\nint total(int pence) {\n    return Shop.priceWithTax(pence);\n}'},
    ("Two changes: add static to the method, and move the 20 into a static final field.", "static final int TAX_PERCENT = 20; static int priceWithTax(int pence) { return pence * (100 + TAX_PERCENT) / 100; }"),
    starter_compiles=False, difficulty=2)
ex.explain("j2-l1.4-explain-equals-hash", "Why both?", ["o3"], ["J2.04"],
    "A teammate overrides `equals` in `Point` so that two points with the same x and y are equal, but leaves `hashCode` alone. Explain the rule that this breaks, why it matters when points are stored in a `HashSet` or used as `HashMap` keys, and what the fix is.",
    "A full answer states that equal objects must return the same hashCode; hash-based collections use hashCode to decide where to look, so two equal points with different hash codes can be looked up in the wrong place and not be found; the fix is to override hashCode from the same fields, for example Objects.hash(x, y).",
    {2: ("States the rule that equal objects must have equal hash codes, explains that hash-based collections use hashCode to choose where to look so equal points could be missed, and gives the fix of hashCode from the same fields.",
         ["The rule is that if two objects are equal according to equals, they must return the same hashCode. HashSet and HashMap use the hash code to decide where to look, so a point equal to one already stored might be looked up in the wrong place and not found. The fix is to override hashCode using the same fields, like Objects.hash(x, y).",
          "It breaks the equals/hashCode contract: equal points need equal hash codes. Without that, a HashSet might say it doesn't contain a point that is equal to one inside, because it looks in the wrong spot. Add a hashCode that uses x and y."]),
     1: ("States the rule or gives the fix but doesn't explain the effect on collections.",
         ["Equal objects need the same hashCode.", "Add a hashCode method."]),
     0: ("Incorrect, for example says hashCode is only for printing or that it doesn't matter.",
         ["hashCode is just for toString.", "It doesn't matter."])})

reg({"j2-l1.4": ("static, toString and equals", ["J2.04"])},
    {"MC35": (["J2.04"], "I38", "Overriding equals without hashCode is fine"),
     "MC36": (["J2.04"], "Platform", "A static field is a good place for each object's own data"),
     "MC37": (["J2.04"], "Platform", "equals(Point other) overrides equals")})
print("2.1 written")
