String classifyExit(int exitCode, boolean oomKilled) {
    if (exitCode == 0) {
        return "ok";
    }
    if (exitCode == 137) {
        return oomKilled ? "kernel-oom-kill" : "killed-by-signal";
    }
    return "application-error";
}

void main() {
}
