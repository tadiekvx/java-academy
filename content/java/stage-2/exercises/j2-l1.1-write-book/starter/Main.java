// Write the class Book here.

String describeBook(String title, int pages) {
    Book b = new Book(title, pages);
    return b.title + " (" + b.pages + " pages)";
}

void main() {
}
