void main() {
    ArrayList<Integer> nums = new ArrayList<>();
    nums.add(30);
    nums.add(10);
    nums.add(20);
    nums.set(1, 99);
    IO.println(nums);
    nums.remove(0);
    IO.println(nums);
    nums.remove(Integer.valueOf(20));
    IO.println(nums + " " + nums.size());
    IO.println(nums.contains(99));
}
