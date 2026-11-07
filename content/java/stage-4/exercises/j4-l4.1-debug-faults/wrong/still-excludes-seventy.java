String report(int[] marks) {
    if (marks.length == 0) {
        return "avg=0 grade=C";
    }
    int total = 0;
    for (int i = 0; i < marks.length; i++) {
        total += marks[i];
    }
    int average = total / marks.length;
    String grade = average > 70 ? "A" : average >= 50 ? "B" : "C";
    return "avg=" + average + " grade=" + grade;
}

void main() {
}
