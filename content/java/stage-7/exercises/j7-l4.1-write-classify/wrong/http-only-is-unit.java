String classify(boolean usesHttp, boolean usesDatabase, boolean needsWholeContext) {
    if (needsWholeContext || (usesHttp && usesDatabase)) {
        return "integration";
    }
    if (usesDatabase) {
        return "slice";
    }
    return "unit";
}

void main() {
}
