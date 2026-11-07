String classifyExit(int exitCode, boolean oomKilled) {
    if (exitCode == 0) {
        return "ok";
    }
    if (oomKilled) {
        return oomKilled ? "kernel-oom-kill" : "killed-by-signal";
    }
    return "application-error";
}

void main() {
}
