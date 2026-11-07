set -e
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
export GIT_AUTHOR_NAME="Ada Learner" GIT_AUTHOR_EMAIL="ada@example.com" GIT_COMMITTER_NAME="Ada Learner" GIT_COMMITTER_EMAIL="ada@example.com"
d=10
stamp() { d=$((d+1)); export GIT_AUTHOR_DATE="2026-11-${d}T10:00:00+0000" GIT_COMMITTER_DATE="2026-11-${d}T10:00:00+0000"; }
commit() { stamp; git commit -q "$@"; }
run() { echo "\$ $*"; "$@" 2>&1 || true; echo; }
cd shop
echo "##### CONFLICT"
git switch -q -c fee-change
sed -i '' 's/120/125/' Price.java
git commit -qam "Raise tax rate to 25%" 2>/dev/null || { stamp; git commit -qam "Raise tax rate to 25%"; }
git switch -q main
sed -i '' 's/120/115/' Price.java
stamp; git commit -qam "Lower tax rate to 15%"
run git merge fee-change
run git status
echo '$ cat Price.java'; cat Price.java; echo
cat > Price.java <<'J'
int withTax(int pence) {
    return pence * 125 / 100;
}

int withDiscount(int pence, int percent) {
    return pence - pence * percent / 100;
}
J
run git add Price.java
echo '$ git commit -m "Merge fee-change: keep the 25% rate"'; stamp; git commit -q -m "Merge fee-change: keep the 25% rate"; echo
run git log --graph --oneline -6
echo "##### REMOTE"
cd ..
git init -q --bare -b main remote.git
cd shop
run git remote add origin ../remote.git
run git remote -v
run git push -u origin main
cd ..
run git clone remote.git clone2
cd clone2
echo "Contributing guide." > CONTRIBUTING.md
git add CONTRIBUTING.md; stamp; git commit -q -m "Add a contributing guide"
run git push
cd ../shop
run git fetch
run git status
run git pull
run git log --oneline -3
echo "##### UNDO"
echo "oops" >> Price.java
run git status --short
run git restore Price.java
run git status --short
run git revert --no-edit HEAD
run git log --oneline -4
run git reset --hard HEAD~1
run git log --oneline -3
run git reflog -5
