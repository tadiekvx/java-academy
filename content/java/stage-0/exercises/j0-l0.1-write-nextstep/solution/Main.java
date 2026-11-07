String nextStep(String fileName) {
    if (fileName.endsWith(".java")) {
        return "javac " + fileName;
    }
    if (fileName.endsWith(".class")) {
        return "java " + fileName.substring(0, fileName.length() - ".class".length());
    }
    return "unknown";
}

void main() {
    IO.println(nextStep("Hello.java")); // should print javac Hello.java
}
