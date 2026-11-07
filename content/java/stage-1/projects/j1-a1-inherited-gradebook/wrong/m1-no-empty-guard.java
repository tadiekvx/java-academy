double average(int[] marks) {
    int total = 0;
    for (int i = 0; i < marks.length; i++) {
        total += marks[i];
    }
    return (double) total / marks.length;
}

String grade(int mark) {
    if (mark >= 70) {
        return "A";
    } else if (mark >= 60) {
        return "B";
    } else if (mark >= 50) {
        return "C";
    } else {
        return "Fail";
    }
}

int countPassing(int[] marks, int passMark) {
    int count = 0;
    for (int i = 0; i < marks.length; i++) {
        if (marks[i] >= passMark) {
            count++;
        }
    }
    return count;
}

int highest(int[] marks) {
    if (marks.length == 0) {
        return -1;
    }
    int best = marks[0];
    for (int mark : marks) {
        if (mark > best) {
            best = mark;
        }
    }
    return best;
}

String summary(int[] marks, int passMark) {
    if (marks.length == 0) {
        return "No students";
    }
    int passed = countPassing(marks, passMark);
    return marks.length + " students, " + passed + " passed (" + passed * 100 / marks.length + "%), highest " + highest(marks);
}

void main() {
    int[] marks = {72, 58, 91, 40};
    IO.println(summary(marks, 50));
}
