long powMod(long base, long exp, long mod) {
    long result = 1 % mod;
    for (long i = 0; i < exp; i++) {
        result = result * (base % mod) % mod;
    }
    return result;
}

void main() {
}
