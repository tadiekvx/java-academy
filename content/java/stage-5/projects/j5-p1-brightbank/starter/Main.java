// Brightbank v5: searching and summarising a very large statement.
// The checks count array reads and enforce a time limit, so the way you search and count matters.
// The methods below compile but return wrong answers. The brief says what each must do.

// Counts how many times get() is called, so the checks can tell a fast search from a slow one.
class CountingArray {
    private final int[] data;
    int reads;

    CountingArray(int[] data) {
        this.data = data;
    }

    int size() {
        return data.length;
    }

    int get(int index) {
        reads++;
        return data[index];
    }
}

int countInRange(CountingArray amounts, int low, int high) {
    return 0;
}

List<String> duplicates(List<String> ids) {
    return new ArrayList<>();
}

List<String> topSpenders(String[] names, int[] pence, int n) {
    return new ArrayList<>();
}

// ---------------------------------------------------------------------------------------------
// The checks call these. They build large inputs for you. Don't change them.
// ---------------------------------------------------------------------------------------------

String m1(int n, int low, int high) {
    int[] data = new int[n];
    for (int i = 0; i < n; i++) {
        data[i] = i * 2;
    }
    CountingArray amounts = new CountingArray(data);
    int count = countInRange(amounts, low, high);
    int limit = 4 * (32 - Integer.numberOfLeadingZeros(Math.max(n, 1))) + 8;
    return count + " fast=" + (amounts.reads <= limit);
}

String m2(int n) {
    int r = Math.min(500, n / 2);
    List<String> ids = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        ids.add("t" + (i < n - r ? i : i - (n - r)));
    }
    List<String> d = duplicates(ids);
    return "size=" + d.size() + " first=" + (d.isEmpty() ? "-" : d.get(0)) + " last=" + (d.isEmpty() ? "-" : d.get(d.size() - 1));
}

String m3(int customers, int n) {
    int count = customers * 3;
    String[] names = new String[count];
    int[] pence = new int[count];
    for (int i = 0; i < count; i++) {
        names[i] = "c" + (i % customers);
        pence[i] = (i * 37) % 1000 + 1;
    }
    return String.join(",", topSpenders(names, pence, n));
}

void main() {
    // Optional: try your methods out here.
}
