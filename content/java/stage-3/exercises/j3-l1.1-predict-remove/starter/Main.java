void main() {
    List<Integer> nums = new ArrayList<>(List.of(10, 20, 30, 20));
    nums.remove(1);
    IO.println(nums);
    nums.remove(Integer.valueOf(20));
    IO.println(nums);
    nums.remove(Integer.valueOf(99));
    IO.println(nums);
    IO.println(nums.contains(30));
}
