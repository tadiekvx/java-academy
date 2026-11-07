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
