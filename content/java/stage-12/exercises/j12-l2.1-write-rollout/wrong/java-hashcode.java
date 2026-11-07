boolean inRollout(String user, String flag, int percent) {
    return Math.floorMod((flag + ":" + user).hashCode(), 100) < percent;
}

void main() {
}
