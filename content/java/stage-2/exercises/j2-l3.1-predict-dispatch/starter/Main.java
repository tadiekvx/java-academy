interface Animal {
    String sound();
}

class Dog implements Animal {
    public String sound() { return "Woof"; }
}

class Cat implements Animal {
    public String sound() { return "Meow"; }
}

class Robot implements Animal {
    public String sound() { return "Beep"; }
}

void main() {
    Animal[] zoo = { new Dog(), new Robot(), new Cat(), new Dog() };
    for (Animal a : zoo) {
        IO.println(a.sound());
    }
    Animal second = zoo[1];
    IO.println(second.sound());
}
