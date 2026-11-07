class Book {
    String title;
    int pages;
    Book(String title, int pages) {
        this.title = title;
    }
}

String describeBook(String title, int pages) {
    Book b = new Book(title, pages);
    return b.title + " (" + b.pages + " pages)";
}

void main() {
}
