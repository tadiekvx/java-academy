String nextStep(String fileName) {
    if (fileName.toLowerCase().endsWith(".java")) {
        return "javac " + fileName;
    }
    if (fileName.endsWith(".class")) {
        return "java " + fileName.substring(0, fileName.length() - 6);
    }
    return "unknown";
}

void main() {
}
