interface Notifier {
    String send(String message);
}

class EmailNotifier implements Notifier {
    public String send(String message) {
        return "email:" + message;
    }
}

class SmsNotifier implements Notifier {
    public String send(String message) {
        return "sms:" + message;
    }
}

class TransferService {
    private final Notifier notifier;

    TransferService(Notifier notifier) {
        this.notifier = notifier;
    }

    String transfer(int cents) {
        return notifier.send("moved " + cents);
    }
}

class FixedService {
    private final Notifier notifier = new EmailNotifier();

    String transfer(int cents) {
        return notifier.send("moved " + cents);
    }
}

void main() {
    System.out.println(new TransferService(new EmailNotifier()).transfer(500));
    System.out.println(new TransferService(new SmsNotifier()).transfer(500));
    System.out.println(new FixedService().transfer(500));
    List<String> sent = new ArrayList<>();
    TransferService tested = new TransferService(m -> {
        sent.add(m);
        return "recorded";
    });
    System.out.println(tested.transfer(75) + " " + sent);
}
