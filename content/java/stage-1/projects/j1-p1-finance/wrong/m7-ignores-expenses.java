int totalExpenses(int[] expenses) {
    int total = 0;
    for (int expense : expenses) {
        total += expense;
    }
    return total;
}

int savings(int income, int[] expenses) {
    return income - totalExpenses(expenses);
}

int savingsRatePercent(int income, int[] expenses) {
    if (income == 0) {
        return 0;
    }
    return savings(income, expenses) * 100 / income;
}

String verdict(int ratePercent) {
    if (ratePercent >= 20) {
        return "Great";
    } else if (ratePercent >= 10) {
        return "Good";
    } else if (ratePercent >= 0) {
        return "Tight";
    } else {
        return "Overspending";
    }
}

String formatMoney(int pence) {
    String sign = pence < 0 ? "-" : "";
    int absolute = Math.abs(pence);
    int pounds = absolute / 100;
    int remainder = absolute % 100;
    String padding = remainder < 10 ? "0" : "";
    return sign + "£" + pounds + "." + padding + remainder;
}

String summary(int income, int[] expenses) {
    int rate = savingsRatePercent(income, expenses);
    return "Income: " + formatMoney(income) + "\n"
            + "Expenses: " + formatMoney(totalExpenses(expenses)) + "\n"
            + "Savings: " + formatMoney(savings(income, expenses)) + " (" + rate + "%) - " + verdict(rate);
}

void main() {
    int income = Integer.parseInt(IO.readln("Monthly income in pence: ").strip());
    ArrayList<Integer> typed = new ArrayList<>();
    String line = IO.readln("Expense in pence (or done): ").strip();
    while (!line.equals("done")) {
        typed.add(0);
        line = IO.readln("Expense in pence (or done): ").strip();
    }
    int[] expenses = new int[typed.size()];
    for (int i = 0; i < expenses.length; i++) {
        expenses[i] = typed.get(i);
    }
    IO.println(summary(income, expenses));
}
