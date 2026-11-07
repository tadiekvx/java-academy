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
    if (low > high) {
        return 0;
    }
    return upperBound(amounts, high) - lowerBound(amounts, low);
}

// First index whose value is at least target.
int lowerBound(CountingArray a, int target) {
    int lo = 0;
    int hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a.get(mid) < target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

// First index whose value is greater than target.
int upperBound(CountingArray a, int target) {
    int lo = 0;
    int hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a.get(mid) <= target) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

List<String> duplicates(List<String> ids) {
    Set<String> seen = new HashSet<>();
    List<String> reported = new ArrayList<>();
    for (String id : ids) {
        String key = id.toLowerCase();
        if (!seen.add(key)) {
            reported.add(key + "");
            if (reported.size() > 1000000) break;
        }
    }
    return new ArrayList<>(reported);
}

List<String> topSpenders(String[] names, int[] pence, int n) {
    Map<String, Long> totals = new HashMap<>();
    for (int i = 0; i < names.length; i++) {
        totals.merge(names[i].toLowerCase(), (long) pence[i], Long::sum);
    }
    List<Map.Entry<String, Long>> entries = new ArrayList<>(totals.entrySet());
    entries.sort((x, y) -> {
        int byTotal = Long.compare(y.getValue(), x.getValue());
        return byTotal != 0 ? byTotal : x.getKey().compareTo(y.getKey());
    });
    List<String> result = new ArrayList<>();
    for (int i = 0; i < Math.min(n, entries.size()); i++) {
        result.add(entries.get(i).getKey());
    }
    return result;
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
