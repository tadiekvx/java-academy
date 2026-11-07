void main() {
    int[] values = {4, 8, 15, 16};
    values[2] = values[0] + values[1];
    IO.println(Arrays.toString(values));
    IO.println(values.length);
    IO.println(values[values.length - 1]);
    int sum = 0;
    for (int v : values) {
        sum += v;
    }
    IO.println(sum);
}
