void main() {
    int price = Integer.parseInt(IO.readln("Price in pence: "));
    int quantity = Integer.parseInt(IO.readln("How many? "));
    IO.println("Total: " + (price * quantity) + " pence");
}
