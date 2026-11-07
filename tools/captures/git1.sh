set -e
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME="Ada Learner" GIT_AUTHOR_EMAIL="ada@example.com" GIT_COMMITTER_NAME="Ada Learner" GIT_COMMITTER_EMAIL="ada@example.com"
d=0
commit() { d=$((d+1)); export GIT_AUTHOR_DATE="2026-11-0${d}T10:00:00+0000" GIT_COMMITTER_DATE="2026-11-0${d}T10:00:00+0000"; git commit -q "$@"; }
run() { echo "\$ $*"; "$@" 2>&1 || true; echo; }
mkdir shop && cd shop
run git init -b main
cat > Price.java <<'J'
int withTax(int pence) {
    return pence * 120 / 100;
}
J
run git status
run git add Price.java
run git status
echo '$ git commit -m "Add the price calculator"'; commit -m "Add the price calculator"; git log --oneline; echo
cat > Price.java <<'J'
int withTax(int pence) {
    return pence * 120 / 100;
}

int withDiscount(int pence, int percent) {
    return pence - pence * percent / 100;
}
J
run git diff
echo '$ git commit -am "Add withDiscount"'; commit -am "Add withDiscount"; echo
run git log --oneline
run git switch -c free-delivery
cat > Delivery.java <<'J'
boolean freeDelivery(int pence) {
    return pence >= 5000;
}
J
git add Delivery.java
echo '$ git commit -am "Add free delivery rule"'; commit -m "Add free delivery rule"; echo
run git switch main
cat > README.md <<'J'
Shop prices.
J
git add README.md
echo '$ git commit -m "Add a README"'; commit -m "Add a README"; echo
run git merge free-delivery -m "Merge free-delivery into main"
run git log --graph --oneline
run git branch
