long powMod(long base, long exp, long mod) {
    if (exp == 0) {
        return 1 % mod;
    }
    long half = powMod(base, exp / 2, mod);
    long result = half * half % mod;
    return result;
}

void main() {
}
