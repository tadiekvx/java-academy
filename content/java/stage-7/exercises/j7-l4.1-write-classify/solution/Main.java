String classify(boolean usesHttp, boolean usesDatabase, boolean needsWholeContext) {
    if (needsWholeContext || (usesHttp && usesDatabase)) {
        return "integration";
    }
    if (usesHttp || usesDatabase) {
        return "slice";
    }
    return "unit";
}

void main() {
}
