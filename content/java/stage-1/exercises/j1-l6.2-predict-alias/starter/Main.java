void main() {
    int[] a = {1, 2, 3};
    int[] b = a;
    int[] c = Arrays.copyOf(a, a.length);
    b[0] = 10;
    c[1] = 20;
    IO.println(Arrays.toString(a));
    IO.println(Arrays.toString(b));
    IO.println(Arrays.toString(c));
    IO.println(a == b);
    IO.println(Arrays.equals(a, c));
}
