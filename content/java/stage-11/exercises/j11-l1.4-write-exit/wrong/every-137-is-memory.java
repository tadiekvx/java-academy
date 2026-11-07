String classifyExit(int exitCode, boolean oomKilled) {
    if (exitCode == 0) {
        return "ok";
    }
    if (exitCode == 137) {
        return "kernel-oom-kill";
    }
    return "application-error";
}

void main() {
}
