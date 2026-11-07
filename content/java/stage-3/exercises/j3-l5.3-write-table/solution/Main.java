String table(String[] names, int[] pence) {
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < names.length; i++) {
        if (i > 0) {
            sb.append("\n");
        }
        String money = "£" + pence[i] / 100 + "." + String.format("%02d", pence[i] % 100);
        sb.append(String.format("%-10s%8s", names[i], money));
    }
    return sb.toString();
}

void main() {
}
