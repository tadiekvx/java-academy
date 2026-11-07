String formatMoney(int pence) {
    String sign = pence < 0 ? "-" : "";
    int absolute = Math.abs(pence);
    String padding = absolute % 100 < 10 ? "0" : "";
    return sign + "£" + absolute / 100 + "." + padding + absolute % 100;
}

int balance(int[] transactions) {
    int total = 0;
    for (int transaction : transactions) {
        total += transaction;
    }
    return total;
}

boolean canWithdraw(int balance, int amount, int overdraftLimit) {
    return amount > 0 && balance - amount >= -overdraftLimit;
}

int[] withTransaction(int[] transactions, int amount) {
    int[] updated = Arrays.copyOf(transactions, transactions.length + 1);
    updated[transactions.length] = amount;
    return updated;
}

String miniStatement(int[] transactions, int count) {
    String text = "";
    int shown = 0;
    for (int i = transactions.length - 1; i >= 0 && shown < count; i--) {
        int amount = transactions[i];
        text += (amount >= 0 ? "Deposit " : "Withdrawal ") + formatMoney(Math.abs(amount)) + "\n";
        shown++;
    }
    return text + "Balance: " + formatMoney(balance(transactions));
}

int dailyWithdrawalRemaining(int[] todaysTransactions, int dailyLimit) {
    int withdrawn = 0;
    for (int transaction : todaysTransactions) {
        if (transaction < 0) {
            withdrawn += -transaction;
        }
    }
    return Math.max(0, dailyLimit - withdrawn);
}

boolean canWithdrawToday(int balance, int amount, int overdraftLimit, int[] todaysTransactions, int dailyLimit) {
    return canWithdraw(balance, amount, overdraftLimit) && amount <= dailyWithdrawalRemaining(todaysTransactions, dailyLimit);
}

void main() {
    int[] history = {10000, -2500};
    history = withTransaction(history, 4000);
    IO.println(miniStatement(history, 2));
}
