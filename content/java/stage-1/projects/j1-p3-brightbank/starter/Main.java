// Brightbank, stage 1: the account logic. Money is whole pence in an int.
// A transaction is positive for a deposit and negative for a withdrawal; an account is its int[] of transactions.
// The methods are stubs that compile but give the wrong answers. The brief and milestones say what each must do.

String formatMoney(int pence) {
    return "";
}

int balance(int[] transactions) {
    return 0;
}

boolean canWithdraw(int balance, int amount, int overdraftLimit) {
    return false;
}

int[] withTransaction(int[] transactions, int amount) {
    return transactions;
}

String miniStatement(int[] transactions, int count) {
    return "";
}

int dailyWithdrawalRemaining(int[] todaysTransactions, int dailyLimit) {
    return 0;
}

boolean canWithdrawToday(int balance, int amount, int overdraftLimit, int[] todaysTransactions, int dailyLimit) {
    return false;
}

void main() {
    // Optional: try your methods out here.
}
