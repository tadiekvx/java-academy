class Student {
    String name;
    int grade;

    Student(String name, int grade) {
        // store the values here
    }
}

String best(String name1, int grade1, String name2, int grade2) {
    Student a = new Student(name1, grade1);
    Student b = new Student(name2, grade2);
    return a.grade >= b.grade ? a.name : b.name;
}

void main() {
}
