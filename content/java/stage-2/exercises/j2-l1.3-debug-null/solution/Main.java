class Player {
    String name;

    Player(String name) {
        this.name = name;
    }
}

class Team {
    Player captain;
}

String captainName(String name, boolean hasCaptain) {
    Team team = new Team();
    if (hasCaptain) {
        team.captain = new Player(name);
    }
    if (team.captain == null) {
        return "none";
    }
    return team.captain.name;
}

void main() {
}
