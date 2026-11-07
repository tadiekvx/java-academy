long sleepersFinished(int count) throws Exception {
    long done = 0;
    for (int i = 0; i < count; i++) {
        Thread.sleep(20);
        done++;
    }
    return done;
}

void main() {
}
