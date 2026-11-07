interface Notifier {
    String send(String message);
}

class Email implements Notifier {
    public String send(String message) {
        return "email: " + message;
    }
}

// Write the class Sms here.

String notifyBy(String channel, String message) {
    Notifier n = channel.equals("email") ? new Email() : new Sms();
    return n.send(message);
}

void main() {
}
