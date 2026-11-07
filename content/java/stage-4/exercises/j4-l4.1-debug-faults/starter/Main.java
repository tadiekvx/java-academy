String report(int[] marks) {
    int total = 0;
    for (int i = 0; i < marks.length - 1; i++) {
        total += marks[i];
    }
    int average = total / marks.length;
    String grade = average > 70 ? "A" : average >= 50 ? "B" : "C";
    return "avg=" + average + " grade=" + grade;
}

void main() {
}
