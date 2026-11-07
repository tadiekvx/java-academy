class Playlist {
    private final List<String> songs;

    Playlist(List<String> songs) {
        this.songs = new ArrayList<>(songs);
    }

    List<String> songs() {
        return new ArrayList<>(songs);
    }

    int size() {
        return songs.size();
    }
}

int run(String[] names) {
    List<String> mine = new ArrayList<>(List.of(names));
    Playlist p = new Playlist(mine);
    mine.add("sneaky");
    try {
        p.songs().add("also sneaky");
    } catch (UnsupportedOperationException e) {
        // an unmodifiable list refused: that is fine
    }
    return p.size();
}

void main() {
}
