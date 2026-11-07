interface Notifier {
    String send(String message);
}

class Email implements Notifier {
    public String send(String message) {
        return "email: " + message;
    }
}

class Sms implements Notifier {
    public String send(String message) {
        String shortened = message.length() > 11 ? message.substring(0, 11) : message;
        return "sms: " + shortened;
    }
}

String notifyBy(String channel, String message) {
    Notifier n = channel.equals("email") ? new Email() : new Sms();
    return n.send(message);
}

void main() {
}
