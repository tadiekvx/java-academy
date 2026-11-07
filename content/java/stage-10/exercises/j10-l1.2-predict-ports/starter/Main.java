interface Ledger {
    void record(String entry);

    List<String> entries();
}

class InMemoryLedger implements Ledger {
    private final List<String> entries = new ArrayList<>();

    public void record(String entry) {
        entries.add(entry);
    }

    public List<String> entries() {
        return entries;
    }
}

class FailingLedger implements Ledger {
    public void record(String entry) {
        throw new IllegalStateException("ledger down");
    }

    public List<String> entries() {
        return List.of();
    }
}

class TransferService {
    private final Ledger ledger;

    TransferService(Ledger ledger) {
        this.ledger = ledger;
    }

    String transfer(String from, String to, int cents) {
        if (cents <= 0) {
            return "rejected";
        }
        try {
            ledger.record(from + "->" + to + ":" + cents);
            return "ok";
        } catch (IllegalStateException e) {
            return "unavailable";
        }
    }
}

void main() {
    InMemoryLedger memory = new InMemoryLedger();
    TransferService working = new TransferService(memory);
    System.out.println(working.transfer("a", "b", 50));
    System.out.println(working.transfer("a", "b", 0));
    System.out.println("entries=" + memory.entries());
    TransferService broken = new TransferService(new FailingLedger());
    System.out.println(broken.transfer("a", "b", 10));
}
