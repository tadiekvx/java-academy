void main() {
    String raw = "POST /api/accounts HTTP/1.1\r\nHost: bank.example\r\nContent-Type: application/json\r\nContent-Length: 15\r\n\r\n{\"owner\":\"Ada\"}";
    String[] parts = raw.split("\r\n\r\n", 2);
    String[] head = parts[0].split("\r\n");
    String[] line = head[0].split(" ");
    System.out.println("method=" + line[0]);
    System.out.println("target=" + line[1]);
    System.out.println("version=" + line[2]);
    System.out.println("headers=" + (head.length - 1));
    for (int i = 1; i < head.length; i++) {
        if (head[i].startsWith("Content-Type:")) {
            System.out.println("type=" + head[i].substring("Content-Type:".length()).trim());
        }
    }
    System.out.println("body chars=" + parts[1].length());
    System.out.println("length matches=" + (parts[1].length() == 15));
}
