String nextStep(String fileName) {
    if (fileName.endsWith(".java")) {
        return "javac " + fileName;
    }
    if (fileName.endsWith(".class")) {
        return "java " + fileName;
    }
    return "unknown";
}

void main() {
}
