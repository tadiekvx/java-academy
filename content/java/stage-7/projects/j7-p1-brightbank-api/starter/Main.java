// Brightbank's API layer as a plain-Java request handler. Each request is "METHOD path body" (the body may be absent).
// Each response is "status|body". Two accounts exist at the start: 1 = Ada Lovelace (120000 cents) and
// 2 = Grace Hopper (30050 cents). Requests are handled in order against the same data.
//
// Milestone 1: routing and reads.   Milestone 2: create and delete.   Milestone 3: replace and deposit.

List<String> handleAll(List<String> requests) {
    List<String> responses = new ArrayList<>();
    for (String request : requests) {
        responses.add("404|Not Found");
    }
    return responses;
}

void main() {
    // Optional: try your handler here.
}
