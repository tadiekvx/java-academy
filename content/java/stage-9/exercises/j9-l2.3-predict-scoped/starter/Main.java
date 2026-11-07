static final ScopedValue<String> USER = ScopedValue.newInstance();

void main() {
    System.out.println("bound before=" + USER.isBound());
    ScopedValue.where(USER, "ada").run(() -> {
        System.out.println("inside=" + USER.get());
        ScopedValue.where(USER, "grace").run(() -> System.out.println("inner=" + USER.get()));
        System.out.println("after inner=" + USER.get());
    });
    System.out.println("bound after=" + USER.isBound());
}
