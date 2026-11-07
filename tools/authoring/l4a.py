import build
build.ROOT = "/Users/brandon/Documents/Java/content/java/stage-4"
from build import *
import outline
reg = outline.register
FOOT = '\nAn exercise counts as **independent** if you pass it with no more help than a nudge, and without viewing a solution.\n'
NOTE = '''
> **How this lesson is assessed.** Git and Maven run on **your own machine**, and this platform can't run them for you. Do the steps in a terminal as you read (the lesson shows real output from a real session). What the platform can check is your **explanations** of what you saw, so the exercises here are written answers.
'''
def explain3(good1, good2, weak, bad):
    return {2: ("Gives a complete and correct answer to every part, using the output shown.", [good1, good2]),
            1: ("Answers some parts correctly, or gives correct points without using the output or without a reason.", [weak, weak[:60]]),
            0: ("Incorrect or off the point, for example describes something different from what the output shows.", [bad])}

# ====================================================================== 4.1.1
Lesson("j4-l1.1", "Snapshots, branches and merging", ["J4.01"], [
    ("o1", "Explain what a commit is, and the roles of the working tree, the staging area and the repository"),
    ("o2", "Read git status, git diff and git log output, including the branch graph"),
    ("o3", "Explain what a branch is, and the difference between a fast-forward and a merge commit"),
], ["j3-l5.3"], 50, ["I61", "I62", "R16"], r'''
## Before you start

You should be comfortable on a command line ([Running Java from the terminal](j0-l0.3)). Check that Git is installed by running `git --version`: if it prints a version, you have it.

**Quick check.** What's the difference between a file you have *saved* and a file you have *committed*?

<details><summary>Show the answer</summary>

A saved file is just on your disk and can be overwritten. A committed file is recorded in the project's history, so you can return to that version.

</details>
''' + NOTE + r'''
## Explanation

### Why version control

Professional code changes constantly, and several people change it at once. **Version control** records every change, who made it and why, so you can see what changed, undo a mistake, and combine work from many people. Git is the tool almost every team uses.

### A commit is a snapshot

Most older systems stored a list of *changes to each file*. **Git thinks in snapshots**: each commit records what the whole project looks like at that moment `[I61]`. Each commit also points back to the commit before it, which is what makes a history.

Git keeps three places, and knowing them explains most of what you'll see `[I61]`:

| Place | What it is |
|---|---|
| **Working tree** | the files on your disk, which you edit |
| **Staging area** | a draft of your *next* commit: what you've chosen to include |
| **Repository** (the Git directory) | the permanent history of commits |

The routine is: edit files, **stage** the changes you want (`git add`), then **commit** them (`git commit`). Staging lets you commit a tidy, related set of changes even if you've edited several things.

### A first repository, with real output

Here is a real session. (I fixed the author and the commit dates so the hashes are the same each time; yours will differ, because a commit's hash depends on its content, author, date and parent.)

```
$ git init -b main
Initialized empty Git repository in .../shop/.git/
```

`git init` turns a folder into a repository, and `-b main` names the first branch `main`. (The Pro Git book says Git's default name is `master`; many teams and hosting services now use `main`.) Now create a file, `Price.java`, and ask what Git sees:

```
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	Price.java

nothing added to commit but untracked files present (use "git add" to track)
```

`Price.java` is **untracked**: it exists in the working tree but Git isn't watching it. Stage it:

```
$ git add Price.java

$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   Price.java
```

It has moved to **Changes to be committed**: it's in the staging area. Commit it, and look at the history:

```
$ git commit -m "Add the price calculator"
$ git log --oneline
9303b85 Add the price calculator
```

`9303b85` is the commit's short **hash**, its identity. `--oneline` shows one commit per line, newest first.

### What changed? `git diff`

After editing `Price.java` again, `git diff` shows exactly what's different from the last commit:

```
$ git diff
diff --git a/Price.java b/Price.java
index 58af79c..fa9dffc 100644
--- a/Price.java
+++ b/Price.java
@@ -1,3 +1,7 @@
 int withTax(int pence) {
     return pence * 120 / 100;
 }
+
+int withDiscount(int pence, int percent) {
+    return pence - pence * percent / 100;
+}
```

Lines starting with `+` were added and lines starting with `-` were removed. Read the diff **before** you commit; it's the cheapest way to catch a stray debug line.

### Commit messages

A commit message is for the person (often you) who reads the history later. Write a short summary line in the **imperative** ("Add the price calculator", "Fix rounding of tax"), saying **what the change does**. If the *why* isn't obvious, add a blank line and a few sentences. `fix`, `update` and `stuff` tell the reader nothing.

### A branch is a pointer

A **branch** is "a lightweight movable pointer" to a commit `[I62]`. Making a branch doesn't copy any files: it adds a new name that points at the same commit. As you commit on a branch, its pointer moves forward. A special pointer, **HEAD**, says which branch you're on `[I62]`.

```
$ git switch -c free-delivery
Switched to a new branch 'free-delivery'
```

`-c` creates the branch and switches to it. Work and commit there, and `main` is untouched. When the work is ready, **merge** it into `main`.

### Merging: fast-forward and merge commits

If `main` hasn't moved since you branched, merging is trivial: Git just moves `main`'s pointer forward to the branch's tip. That's a **fast-forward** `[I62]`: no new commit is needed.

If both `main` and the branch have new commits, Git combines the two histories and records a **merge commit** with two parents. In my session, `main` got a README commit while `free-delivery` got a delivery-rule commit:

```
$ git merge free-delivery -m "Merge free-delivery into main"
Merge made by the 'ort' strategy.
 Delivery.java | 3 +++
 1 file changed, 3 insertions(+)
 create mode 100644 Delivery.java
```

`git log --graph --oneline` draws the history:

```
$ git log --graph --oneline
*   8ef0284 Merge free-delivery into main
|\
| * 78ee5d6 Add free delivery rule
* | 1736485 Add a README
|/
* e506a4b Add withDiscount
* 9303b85 Add the price calculator
```

Read it from the top: the merge commit `8ef0284` has two parents (the two lines it joins). Below the split, one line is `main`'s README commit and the other is the branch's delivery commit. Both came from `e506a4b`, where the branch was made.

## Worked examples

### Example 1: reading the staging output

*Task: after `git add Price.java`, `git status` says "Changes to be committed". What does that tell you?*

**Step 1 — Which of the three places holds the change?** The staging area: it's ready for the next commit.

**Step 2 — Is it in the history yet?** No. Until `git commit`, it can still be changed or unstaged.

**Step 3 — What's the next command?** `git commit -m "..."`.

### Example 2: improving a message

*Task: improve the commit message "update stuff" for a change that adds a 10% member discount.*

**Step 1 — What does the change do?** It adds a discount for members.

**Step 2 — Write it in the imperative, with the point:** `Add 10% discount for members`.

**Step 3 — Does the reader need the why?** If the rule came from a ticket, add: a blank line, then `Requested in ticket 214: loyalty scheme launch.`

## Where this is used

- **Every software team**, from two people to thousands, uses Git or a tool like it.
- **Debugging:** when something broke, the history says when and why a line changed.
- **Code review** works on branches and diffs.

## Common mistakes

:::mistake{id=MC130}
**Thinking `git add` saves the change permanently.** It only stages it. Nothing is in the history until you commit.
:::

:::mistake{id=MC131}
**Thinking a branch is a copy of all the files.** It's a pointer to a commit, which is why branching is instant and cheap.
:::

:::mistake{id=MC132}
**Vague commit messages** (`fix`, `update`, `wip`). They make the history useless for finding out what changed and why.
:::

## Practice

::exercise{id=j4-l1.1-explain-status}

::exercise{id=j4-l1.1-explain-graph}

::exercise{id=j4-l1.1-explain-messages}

## Further reading

- **Pro Git, "What is Git?"** `[I61]` explains snapshots and the three places.
- **Pro Git, "Branches in a Nutshell" and "Basic Branching and Merging"** `[I62]` explain pointers, fast-forwards and merges, with diagrams.
- **McCauley et al. (2008)** `[R16]` on debugging: a history of small, well-described commits is evidence for finding when a bug appeared.

## How you'll be assessed

- The **explain** exercises check that you can read Git's output and describe commits, staging and branch history in your own words (*explanation*).
''' + FOOT)

ex = Exercises("j4-l1.1")
ex.explain("j4-l1.1-explain-status", "What did git add do?", ["o1", "o2"], ["J4.01"],
    "A learner creates `Price.java` in a new repository and runs `git status`, which shows:\n\n```\nUntracked files:\n\tPrice.java\n```\n\nThey run `git add Price.java` and `git status` again:\n\n```\nChanges to be committed:\n\tnew file:   Price.java\n```\n\n(a) Which of the three places (working tree, staging area, repository) holds the file before and after `git add`? (b) Is the file in the project's history now? (c) What single command would put it there, and what should the learner give it?",
    "A full answer says the file is only in the working tree (untracked) before git add, and in the staging area as well after it; it isn't in the history until git commit; and the command is git commit with a short, imperative message describing the change.",
    {2: ("Says untracked means working tree only, after git add it is staged (in the staging area), it is not yet in the repository history, and git commit -m with a clear imperative message puts it there.",
         ["Before git add the file is only in the working tree: Git sees it but isn't tracking it. After git add it's in the staging area, ready for the next commit. It isn't in the history yet, because that only happens at commit. git commit -m \"Add the price calculator\" would record it, with a short message saying what the change does.",
          "(a) Working tree only, then working tree plus staging area. (b) No, staged isn't committed. (c) git commit with a message such as \"Add price calculator\"."]),
     1: ("Gets some parts right, for example the staging area but not that it isn't committed, or no mention of the message.",
         ["It's staged now.", "Run git commit."]),
     0: ("Incorrect, for example says git add commits the file, or that the file is in the repository after git add.",
         ["git add saved it permanently into the history.", "It was committed by git add."])})
ex.explain("j4-l1.1-explain-graph", "Read the history", ["o2", "o3"], ["J4.01"],
    "This is the output of `git log --graph --oneline` in a repository:\n\n```\n*   8ef0284 Merge free-delivery into main\n|\\\n| * 78ee5d6 Add free delivery rule\n* | 1736485 Add a README\n|/\n* e506a4b Add withDiscount\n* 9303b85 Add the price calculator\n```\n\n(a) Which commit is the merge commit, and how many parents does it have? (b) From which commit did the two lines of work split? (c) Why did this merge create a commit, where a merge that Git can fast-forward doesn't? (d) What is a branch, in terms of these commits?",
    "A full answer says 8ef0284 is the merge commit with two parents (78ee5d6 and 1736485); the work split at e506a4b; both main (the README commit) and the free-delivery branch had their own new commits, so Git had to combine them, whereas a fast-forward is only possible when the target hasn't moved; and a branch is a movable pointer to one of these commits.",
    {2: ("Identifies 8ef0284 as the merge commit with two parents, e506a4b as the split point, explains both lines had new commits so a merge commit was needed (a fast-forward only moves a pointer when one side hasn't moved), and says a branch is a pointer to a commit.",
         ["(a) 8ef0284 is the merge commit, and it has two parents: the free-delivery commit 78ee5d6 and the README commit 1736485. (b) They split at e506a4b, Add withDiscount. (c) main had its own new commit (the README) as well as the branch, so Git had to combine two lines of work with a merge commit; a fast-forward only works when main hasn't moved. (d) A branch is a movable pointer to a commit.",
          "The merge commit is 8ef0284 with two parents. Both lines come from e506a4b. Because both sides had new commits, a merge commit was needed rather than a fast-forward. A branch is just a pointer to a commit."]),
     1: ("Answers some parts, for example finds the merge commit but not why it was needed, or doesn't say what a branch is.",
         ["8ef0284 is the merge.", "It split earlier."]),
     0: ("Incorrect, for example says the merge commit is the oldest one, or that a branch is a copy of the files.",
         ["The merge commit is 9303b85.", "A branch is a folder copy of the project."])})
ex.explain("j4-l1.1-explain-messages", "Write better messages", ["o1"], ["J4.01"],
    "Three commit messages from a repository's history are: `update`, `fixed it`, and `Changes to Price.java`. (a) Say what is wrong with them, in terms of what a reader needs. (b) Rewrite each one, assuming the changes were, in order: adding a 10% discount for members; fixing a rounding error that made tax too low by 1 penny on odd prices; and renaming `withTax` to `priceWithTax`. (c) Say when a message needs more than one line.",
    "A full answer says the messages don't say what changed or why so the history can't be used to find a change; gives imperative summaries such as Add 10% discount for members, Fix tax rounding on odd prices, Rename withTax to priceWithTax; and says a longer body is needed when the reason isn't obvious from the summary.",
    {2: ("Says the messages don't say what changed or why, gives three clear imperative rewrites matching the three changes, and says a body is needed when the reason isn't obvious from the summary line.",
         ["They don't say what changed or why, so someone searching the history later can't tell which commit did what. Better: \"Add 10% discount for members\", \"Fix tax rounding on odd prices\", \"Rename withTax to priceWithTax\". A message needs more than one line when the summary doesn't make the reason obvious, for example a bug fix that needs the cause explained.",
          "(a) Too vague to tell what changed or why. (b) Add member discount of 10%; Fix 1p rounding error in tax on odd prices; Rename withTax to priceWithTax. (c) Add a body when the why isn't obvious."]),
     1: ("Gives rewrites without explaining the problem, or explains the problem without good rewrites.",
         ["They're too vague.", "Add member discount."]),
     0: ("Incorrect, for example says short vague messages are best, or rewrites them in ways that don't match the changes.",
         ["Short messages like update are best.", "Use the file name as the message."])})
reg({"j4-l1.1": ("Snapshots, branches and merging", ["J4.01"])},
    {"MC130": (["J4.01"], "I61", "git add saves a change permanently into the history"),
     "MC131": (["J4.01"], "I62", "A branch is a full copy of the project's files"),
     "MC132": (["J4.01"], "Platform", "A commit message such as 'fix' or 'update' is good enough")})

# ====================================================================== 4.1.2
Lesson("j4-l1.2", "Conflicts, remotes and undoing safely", ["J4.02"], [
    ("o1", "Read a merge conflict, resolve it, and know how to back out of a merge"),
    ("o2", "Describe the clone, push, fetch and pull cycle and what origin is"),
    ("o3", "Choose the right way to undo a change, and say which ways are safe on shared history"),
], ["j4-l1.1"], 55, ["I62", "I63", "I64", "R16"], r'''
## Before you start

You should know what a commit, a branch and a merge are ([Snapshots, branches and merging](j4-l1.1)).

**Quick check.** When can Git do a **fast-forward** merge?

<details><summary>Show the answer</summary>

When the branch you're merging into hasn't moved since the other branch was made, so Git can just move its pointer forward.

</details>
''' + NOTE + r'''
## Explanation

### Conflicts

Git merges two lines of work automatically, **unless both changed the same lines**. Then it can't know which to keep, and stops. That's a **merge conflict**. It isn't an error in your repository; it's Git asking you to decide.

In my session, `main` changed the tax rate to 15% while the branch `fee-change` changed the same line to 25%:

```
$ git merge fee-change
Auto-merging Price.java
CONFLICT (content): Merge conflict in Price.java
Automatic merge failed; fix conflicts and then commit the result.

$ git status
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   Price.java

no changes added to commit (use "git commit -a")
```

Git has paused the merge `[I62]` and tells you the options. Open the file and you'll find **conflict markers**:

```
int withTax(int pence) {
<<<<<<< HEAD
    return pence * 115 / 100;
=======
    return pence * 125 / 100;
>>>>>>> fee-change
}
```

Between `<<<<<<< HEAD` and `=======` is **your side** (the branch you're on, `main`); between `=======` and `>>>>>>> fee-change` is **the other side** `[I62]`. To resolve it:

1. **Edit the file** so it contains what you really want: pick one side, combine them, or write something new. **Delete all three marker lines.**
2. **`git add Price.java`** to say it's resolved.
3. **`git commit`** to finish the merge.

```
$ git add Price.java
$ git commit -m "Merge fee-change: keep the 25% rate"
$ git log --graph --oneline -6
*   91326d7 Merge fee-change: keep the 25% rate
|\
| * 1b94a7a Raise tax rate to 25%
* | ed61a4a Lower tax rate to 15%
|/
*   8ef0284 Merge free-delivery into main
...
```

If you're unsure, **back out**: `git merge --abort` (offered in the status output) returns to how things were before the merge. Never leave the markers in a file you commit: they'd break the code.

The real work is **deciding**, not editing. If you can't tell which side is right, ask the person who made the other change. Conflicts are fewer when branches are short-lived and you merge often.

### Remotes: sharing work

A **remote** is another copy of the repository, usually on a server (GitHub, GitLab or your company's), that everyone shares. `origin` is the default name Git gives the server you cloned from `[I64]`. To keep this lesson on one machine, my "server" is just a second repository created with `git init --bare` (a repository with no working tree, which is what servers hold).

```
$ git remote add origin ../remote.git
$ git remote -v
origin	../remote.git (fetch)
origin	../remote.git (push)

$ git push -u origin main
To ../remote.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

`git push` sends your commits to the remote. `-u` also remembers that your `main` tracks `origin/main`, so later `git push` and `git pull` need no arguments.

A colleague clones the repository, makes a commit, and pushes:

```
$ git clone remote.git clone2
Cloning into 'clone2'...
done.
```

Back in the first repository, you don't see their commit until you ask:

```
$ git fetch
From ../remote
   91326d7..19328b5  main       -> origin/main

$ git status
On branch main
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)

nothing to commit, working tree clean
```

`git fetch` **downloads** new commits (into `origin/main`) but doesn't change your own branch. `git status` now says you're behind by one commit. `git pull` fetches **and then merges** the remote branch into your current branch `[I64]`:

```
$ git pull
Updating 91326d7..19328b5
Fast-forward
 CONTRIBUTING.md | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 CONTRIBUTING.md
```

It was a fast-forward, because you hadn't moved. If you *had* committed in the meantime, `pull` would merge (and could conflict). A good habit: **pull before you start work**, and push small changes often.

### Pull requests

A **pull request** (PR) is a feature of hosting services such as GitHub, not of Git itself. You push a branch and ask your team to review it before it's merged into `main`. A good PR is small, has a clear title, and a description that says **what** changed, **why**, and **how it was tested**, so that reviewers can focus on whether it's right.

### Undoing things

Mistakes happen. Which command to use depends on **how far the mistake has gone**:

| Situation | Command | Notes |
|---|---|---|
| Edited a file, want the last committed version back | `git restore Price.java` | discards your uncommitted edits to that file `[I63]` |
| Last commit is wrong or incomplete, and not shared | `git commit --amend` | redoes the last commit `[I63]` |
| A bad commit is already **shared** | `git revert <commit>` | adds a **new** commit that undoes it; history isn't rewritten |
| A local commit should vanish, and isn't shared | `git reset --hard HEAD~1` | moves the branch back and **discards** the commit's changes |

```
$ echo "oops" >> Price.java
$ git status --short
 M Price.java
$ git restore Price.java
$ git status --short
$ git revert --no-edit HEAD
[main 0a0d4ea] Revert "Add a contributing guide"
 1 file changed, 1 deletion(-)
 delete mode 100644 CONTRIBUTING.md
```

After the revert the history has **both** the original commit and the commit that undoes it:

```
$ git log --oneline -4
0a0d4ea Revert "Add a contributing guide"
19328b5 Add a contributing guide
91326d7 Merge fee-change: keep the 25% rate
ed61a4a Lower tax rate to 15%
```

That's why `revert` is the safe choice for shared history: nobody else's copy has to change. By contrast `reset --hard` and `--amend` **rewrite** history. Do that only to commits nobody else has pulled, because everyone who has them would then have to repair their copies.

### A safety net: the reflog

Even `reset --hard` isn't always final. Git keeps a log of where your branch tip has been, the **reflog**:

```
$ git reset --hard HEAD~1
HEAD is now at 19328b5 Add a contributing guide

$ git reflog -5
19328b5 HEAD@{0}: reset: moving to HEAD~1
0a0d4ea HEAD@{1}: revert: Revert "Add a contributing guide"
19328b5 HEAD@{2}: pull: Fast-forward
91326d7 HEAD@{3}: commit (merge): Merge fee-change: keep the 25% rate
ed61a4a HEAD@{4}: commit: Lower tax rate to 15%

$ git reset --hard 0a0d4ea
HEAD is now at 0a0d4ea Revert "Add a contributing guide"
```

The commit that "disappeared" was still there, listed as `HEAD@{1}`. Resetting to its hash brought it back. Uncommitted edits discarded by `git restore` or `reset --hard` have **no** such safety net, which is another reason to commit early.

## Worked examples

### Example 1: resolving the conflict

*Task: the file shows 115 on your side and 125 on theirs. The team agreed on 25%. What do you do?*

**Step 1 — Edit the file:** keep `return pence * 125 / 100;` and delete the markers and the 115 line.

**Step 2 — Mark it resolved:** `git add Price.java`.

**Step 3 — Finish the merge:** `git commit`, with a message that says what you decided.

### Example 2: which undo?

*Task: you pushed a commit an hour ago and now realise it breaks the build. Colleagues have pulled it. Which command?*

**Step 1 — Is the commit shared?** Yes.

**Step 2 — So don't rewrite history:** use `git revert <commit>`.

**Step 3 — Push the revert commit.** Everyone's next `pull` just receives one more commit.

## Where this is used

- **Teamwork:** conflicts, pulls and pushes happen every day on any shared repository.
- **Incidents:** reverting a bad release is a standard first response.
- **Reviews:** a clean branch with clear commits and a good PR description is what reviewers expect.

## Common mistakes

:::mistake{id=MC133}
**Committing a file that still has conflict markers.** The `<<<<<<<` lines are not valid code. Resolve, test, then commit.
:::

:::mistake{id=MC134}
**Using `git reset --hard` or `--amend` on commits others have already pulled.** It rewrites shared history. Use `git revert`.
:::

:::mistake{id=MC135}
**Treating `git fetch` as if it updated your branch.** It only downloads. Your branch changes when you merge (or `pull`).
:::

## Practice

::exercise{id=j4-l1.2-explain-conflict}

::exercise{id=j4-l1.2-explain-remote}

::exercise{id=j4-l1.2-explain-undo}

## Further reading

- **Pro Git, "Basic Branching and Merging"** `[I62]` walks through a conflict and its markers.
- **Pro Git, "Undoing Things"** `[I63]` covers `restore` and `--amend`.
- **Pro Git, "Working with Remotes"** `[I64]` covers `origin`, `fetch` and `pull`.
- **McCauley et al. (2008)** `[R16]` on debugging: `git log` and `git diff` between two commits narrow down where a bug appeared.

## How you'll be assessed

- The **explain** exercises check that you can read a conflict and its markers, describe the fetch/pull cycle, and choose a safe way to undo a mistake (*explanation*).
''' + FOOT)

ex = Exercises("j4-l1.2")
ex.explain("j4-l1.2-explain-conflict", "Resolve it", ["o1"], ["J4.02"],
    "After `git merge fee-change`, Git says `CONFLICT (content): Merge conflict in Price.java` and the file contains:\n\n```\nint withTax(int pence) {\n<<<<<<< HEAD\n    return pence * 115 / 100;\n=======\n    return pence * 125 / 100;\n>>>>>>> fee-change\n}\n```\n\n(a) What do the three marker lines and the two code lines mean? (b) Give the steps to resolve it, once the team has agreed on 25%. (c) What command backs out of the merge if you'd rather start again, and what would be wrong with committing the file as it is?",
    "A full answer says the section between <<<<<<< HEAD and ======= is the current branch's version (115) and between ======= and >>>>>>> fee-change is the other branch's (125); the steps are to edit the file to the intended version deleting all three marker lines, git add the file, and git commit; git merge --abort backs out; and committing with markers would put invalid text into the code and break the build.",
    {2: ("Explains that the top section is the current branch's version (115) and the bottom is fee-change's (125), gives edit-add-commit with all markers deleted, names git merge --abort, and says committing the markers would break the code.",
         ["The part between <<<<<<< HEAD and ======= is my branch's version (15%), and the part between ======= and >>>>>>> fee-change is the other branch's (25%). To resolve it I edit the file to keep the 125 line and delete all three marker lines, then git add Price.java and git commit. git merge --abort goes back to before the merge. If I committed the file with the markers, the lines wouldn't be valid Java and the build would break.",
          "(a) HEAD side is main's 115 and the other side is fee-change's 125. (b) Edit to the 125 version, remove the markers, git add, git commit. (c) git merge --abort; committing markers would leave invalid code in the file."]),
     1: ("Answers some parts, for example the steps without explaining the markers, or no mention of abort or of the risk.",
         ["Edit the file and commit.", "Use git merge --abort."]),
     0: ("Incorrect, for example says to commit the file as it is, or that the markers are code to keep.",
         ["Just commit the file, the markers are fine.", "Delete the file."])})
ex.explain("j4-l1.2-explain-remote", "Fetch, status, pull", ["o2"], ["J4.02"],
    "A colleague pushed a commit to the shared repository. In your own copy you run:\n\n```\n$ git fetch\nFrom ../remote\n   91326d7..19328b5  main       -> origin/main\n\n$ git status\nOn branch main\nYour branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.\n\n$ git pull\nUpdating 91326d7..19328b5\nFast-forward\n```\n\n(a) What does `origin` refer to? (b) What did `git fetch` do, and what did it not do? (c) Why does `git status` say you're behind, and what did `git pull` do about it? (d) Why was the pull a fast-forward?",
    "A full answer says origin is the default name for the remote server repository you cloned from; fetch downloaded the new commit into origin/main without changing your own main branch; status says behind because origin/main has a commit your branch lacks, and pull fetched and merged it into your branch; and it was a fast-forward because you had no commits of your own since, so Git just moved your branch pointer forward.",
    {2: ("Says origin is the default name of the remote you cloned from, fetch downloaded the commit into origin/main but didn't change your branch, status reports behind because origin/main is ahead, pull fetches and merges it, and fast-forward happened because you had no new local commits.",
         ["Origin is the default name for the shared repository I cloned from. git fetch downloaded the colleague's commit into origin/main but left my own main alone. Status says I'm behind because origin/main has one commit my main doesn't. git pull fetches and merges it into my branch. It was a fast-forward because I hadn't made any commits since, so Git just moved my pointer forward.",
          "origin is the remote. fetch only downloads. behind by 1 commit means the remote has something I don't. pull merges it, and it fast-forwarded because my branch hadn't diverged."]),
     1: ("Answers some parts, for example what pull does but not what fetch leaves alone, or no reason for the fast-forward.",
         ["Pull gets the new commit.", "origin is the server."]),
     0: ("Incorrect, for example says fetch updates your branch, or that origin is your local branch.",
         ["fetch merges the changes into my branch.", "origin is my own main branch."])})
ex.explain("j4-l1.2-explain-undo", "Which undo?", ["o3"], ["J4.02"],
    "For each situation, say which command you'd use, and whether it is safe to use if other people already have the commit: (a) you edited `Price.java`, haven't committed, and want the last committed version back; (b) you committed a change that breaks the build, **and pushed it**, and colleagues have pulled; (c) you made a commit locally by mistake and haven't pushed it. Then (d) you ran `git reset --hard HEAD~1` and lost a commit you needed: how can you get it back?",
    "A full answer says git restore for (a) (it only discards uncommitted edits); git revert for (b) because it adds a new commit and doesn't rewrite shared history; git reset --hard HEAD~1 (or amend) for (c) since nobody else has the commit; and for (d) use git reflog to find the commit's hash and git reset --hard to that hash.",
    {2: ("Gives git restore for (a), git revert for (b) explaining it adds a commit and doesn't rewrite shared history, reset --hard HEAD~1 or amend for (c) because it isn't shared, and git reflog then reset to the hash for (d).",
         ["(a) git restore Price.java, which discards my uncommitted edits. (b) git revert on that commit, because it adds a new commit that undoes it and doesn't rewrite history others already have. (c) git reset --hard HEAD~1 is fine because nobody else has the commit, as long as I really want to discard it. (d) git reflog shows where HEAD has been, so I find the lost commit's hash and git reset --hard to it.",
          "a: restore. b: revert, safe for shared commits since it adds history. c: reset --hard HEAD~1 or amend, since it's not pushed. d: look in git reflog for the hash and reset back to it."]),
     1: ("Gets two or three of the four right, or names commands without the safety reasoning.",
         ["(a) git restore (b) git reset --hard (c) git revert.", "Use git reflog."]),
     0: ("Incorrect, for example says to use reset --hard on shared commits, or that a reset commit is gone for good.",
         ["(b) git reset --hard HEAD~1 and force push.", "A reset commit can never be recovered."])})
reg({"j4-l1.2": ("Conflicts, remotes and undoing safely", ["J4.02"])},
    {"MC133": (["J4.02"], "I62", "A file with conflict markers can be committed as it is"),
     "MC134": (["J4.02"], "Platform", "Resetting or amending commits that others have pulled is safe"),
     "MC135": (["J4.02"], "I64", "git fetch updates the branch you are on")})

# ====================================================================== 4.2.1
Lesson("j4-l2.1", "Maven: project layout and the POM", ["J4.03"], [
    ("o1", "Say where source code, tests and compiled output live in a Maven project"),
    ("o2", "Read a pom.xml: coordinates, properties, dependencies with scopes, and plugins"),
    ("o3", "Explain why real projects use a build tool instead of running javac by hand"),
], ["j4-l1.2"], 45, ["I67", "I66", "R8"], r'''
## Before you start

You can compile and run a Java file from the terminal ([Running Java from the terminal](j0-l0.3)), and you know packages and classes ([Classes and objects](j2-l1.1)).

**Quick check.** What does `javac Hello.java` produce?

<details><summary>Show the answer</summary>

`Hello.class`, the compiled bytecode.

</details>
''' + NOTE + r'''
## Explanation

### Why a build tool

Running `javac` by hand works for one file. A real project has hundreds of source files in packages, **libraries** written by other people (each with its own libraries), tests to run, and a **jar file** to produce. Doing that by hand, the same way on every developer's machine and on the build server, is impossible. A **build tool** does it from a description in a file.

**Maven** is the most widely used build tool for Java. You describe the project in a file called **`pom.xml`** (the Project Object Model), and Maven compiles, tests, packages, and fetches the libraries you ask for, in a standard way.

### A standard layout

Maven works because every project is arranged the same way `[I67]`. A real, tiny project from my machine:

```
shop/
  pom.xml
  src/
    main/java/com/example/shop/Price.java
    test/java/com/example/shop/PriceTest.java
```

- **`src/main/java`** holds the application's sources `[I67]`.
- **`src/test/java`** holds the tests `[I67]`.
- The **folders under `java` mirror the package**: `com.example.shop.Price` lives in `com/example/shop/Price.java`.
- **`pom.xml`** sits at the top `[I67]`.
- After a build, a **`target`** directory appears with the compiled classes, test reports and the jar. It is generated: never edit it, and don't commit it to version control.

Because everyone uses the same layout, a new colleague can open any Maven project and know where things are.

### Reading a POM

Here is the whole `pom.xml` of that project:

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0" ...>
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>shop</artifactId>
  <version>1.0-SNAPSHOT</version>

  <properties>
    <maven.compiler.release>25</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>6.1.3</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.6</version>
      </plugin>
    </plugins>
  </build>
</project>
```

| Part | What it says |
|---|---|
| `groupId`, `artifactId`, `version` | the project's **coordinates**: a unique address. `groupId` is usually a reversed domain name, `artifactId` the project name. Every library on Maven Central is found by these three. |
| `1.0-SNAPSHOT` | a version still in development. A release has a fixed number such as `1.0`. |
| `<properties>` | settings. `maven.compiler.release` is the Java version to compile for (25 here). `sourceEncoding` is the character set of your files. |
| `<dependencies>` | libraries the project uses. Maven downloads them (and *their* dependencies) from a repository. |
| `<scope>test</scope>` | the library is only used for tests. It isn't on the classpath of the main code, and won't be in the app you ship `[I66]`. |
| `<build><plugins>` | tools that do the work. The **compiler** plugin compiles; the **surefire** plugin runs your tests; the **jar** plugin packages. |

Version numbers for libraries change; when you add a dependency, take its current version from the library's own page or from Maven Central. The `junit-jupiter` version above (6.1.3) was the latest release when I wrote this.

### Dependency scope

A dependency's **scope** limits where it's available `[I66]`. Two you'll use constantly: the default (`compile`) means available everywhere in the project, and `test` means only for compiling and running tests. A testing library has no business inside the product.

## Worked examples

### Example 1: where does this file go?

*Task: a test class `com.example.shop.PriceTest` and a main class `com.example.shop.Price`. Where do they live?*

**Step 1 — Main code:** `src/main/java/com/example/shop/Price.java`.

**Step 2 — Test code:** `src/test/java/com/example/shop/PriceTest.java`.

**Step 3 — Why the same package?** It lets the test see package-private members, and keeps related files together.

### Example 2: reading a dependency

*Task: what does this declare?*

```xml
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-text</artifactId>
  <version>1.11.0</version>
</dependency>
```

**Step 1 — Coordinates:** library `commons-text` from group `org.apache.commons`, version 1.11.0.

**Step 2 — Scope:** none given, so `compile`: available to the main code and the tests.

**Step 3 — Its own dependencies:** Maven also downloads whatever `commons-text` depends on (next lesson).

## Where this is used

- **Almost every Java project** at work is a Maven or Gradle project, so reading a `pom.xml` is a basic professional skill.
- **Continuous integration** servers run the same build from the same file as you do.
- **Frameworks** such as Spring Boot (Stage 7) are added to a project as dependencies in its POM.

## Common mistakes

:::mistake{id=MC136}
**Putting tests in `src/main/java`** (or code in `src/test/java`). Maven only runs tests found under `src/test/java`, and would ship test code with the application.
:::

:::mistake{id=MC137}
**Committing the `target` directory.** It is generated output. Others will rebuild it, and it only creates noise and conflicts.
:::

:::mistake{id=MC138}
**Forgetting `<scope>test</scope>` on a test library.** It then becomes part of the application's own dependencies.
:::

## Practice

::exercise{id=j4-l2.1-explain-layout}

::exercise{id=j4-l2.1-explain-pom}

::exercise{id=j4-l2.1-explain-why}

## Further reading

- **Maven, "Introduction to the Standard Directory Layout"** `[I67]` lists the directories.
- **Maven, "Introduction to the Dependency Mechanism"** `[I66]` covers dependencies and scopes.
- **Qian & Lehman (2017)** `[R8]` on how learners move from single files to multi-file programs.

## How you'll be assessed

- The **explain** exercises check that you can say where files belong in a Maven project, read a POM, and explain why a build tool exists (*explanation*).
''' + FOOT)

ex = Exercises("j4-l2.1")
ex.explain("j4-l2.1-explain-layout", "Where does it go?", ["o1"], ["J4.03"],
    "A Maven project contains:\n\n```\nshop/\n  pom.xml\n  src/main/java/com/example/shop/Price.java\n  src/test/java/com/example/shop/PriceTest.java\n  target/shop-1.0-SNAPSHOT.jar\n```\n\n(a) Which file is the application's own code, and which is a test? How does Maven tell them apart? (b) Why is the folder path `com/example/shop`? (c) What is in `target`, and should it go into version control?",
    "A full answer says Price.java under src/main/java is the application code and PriceTest.java under src/test/java is the test, which Maven distinguishes by the directory; the folders mirror the package com.example.shop; and target holds generated output (compiled classes, test reports and the jar) so it shouldn't be committed.",
    {2: ("Identifies Price.java as application code and PriceTest.java as a test by their directories, says the folder path mirrors the package name, and says target is generated build output that shouldn't be in version control.",
         ["Price.java is the application code and PriceTest.java is the test: Maven tells them apart by directory, src/main/java versus src/test/java. The folders com/example/shop mirror the package com.example.shop. target holds generated output such as compiled classes, test reports and the jar, so it shouldn't be committed.",
          "(a) Price.java in src/main is the app; PriceTest.java in src/test is the test. (b) The path matches the package name. (c) target is build output, so keep it out of version control."]),
     1: ("Answers two parts, or answers all but without reasons.",
         ["Price is the app and PriceTest is the test.", "target is output."]),
     0: ("Incorrect, for example says target is where you write your code or that tests go in src/main.",
         ["Put your code in target.", "Both files are application code."])})
ex.explain("j4-l2.1-explain-pom", "Read the POM", ["o2"], ["J4.03"],
    "A POM contains:\n\n```xml\n<groupId>com.example</groupId>\n<artifactId>shop</artifactId>\n<version>1.0-SNAPSHOT</version>\n<properties>\n  <maven.compiler.release>25</maven.compiler.release>\n</properties>\n<dependency>\n  <groupId>org.junit.jupiter</groupId>\n  <artifactId>junit-jupiter</artifactId>\n  <version>6.1.3</version>\n  <scope>test</scope>\n</dependency>\n```\n\n(a) What do `groupId`, `artifactId` and `version` together identify, and what does `SNAPSHOT` signal? (b) What does `maven.compiler.release` control? (c) What does `<scope>test</scope>` mean, and why is it right for JUnit?",
    "A full answer says the three coordinates form a unique address for the project (or library); SNAPSHOT means a version still under development; maven.compiler.release sets the Java version the code is compiled for; and test scope means the library is only available when compiling and running tests, which is right because testing code doesn't belong in the shipped application.",
    {2: ("Says the coordinates identify the project uniquely, SNAPSHOT means in development, maven.compiler.release is the Java version to compile for, and test scope limits JUnit to the tests so it isn't shipped with the application.",
         ["Together they're a unique address for the project: the group, the name and the version. SNAPSHOT means it's still being developed, not a fixed release. maven.compiler.release is the Java version to compile for, here 25. test scope means JUnit is only used when compiling and running tests, which is right because test code shouldn't be shipped in the application.",
          "(a) The project's coordinates; SNAPSHOT is a development version. (b) The Java release the code compiles for. (c) Only for tests, so JUnit isn't part of the real app."]),
     1: ("Answers two parts correctly, or gives correct points without the reasons.",
         ["It's the project's name and version.", "Test scope is for tests."]),
     0: ("Incorrect, for example says test scope makes the dependency run slower, or that SNAPSHOT means a backup.",
         ["SNAPSHOT is a backup copy.", "Test scope means the library is tested."])})
ex.explain("j4-l2.1-explain-why", "Why not just javac?", ["o3"], ["J4.03"],
    "A new teammate asks: \"Why do we need Maven? I can just run `javac` on all the files.\" Give **three** concrete things a build tool does for a real project that running `javac` by hand does not, and say why the file that describes the build (`pom.xml`) is useful to the whole team.",
    "A full answer gives three things such as downloading and managing library dependencies (and their dependencies), running the tests as part of the build, packaging a jar, and building the same way on every machine through a standard layout and lifecycle; and says the POM is a single shared description so everyone and the build server build identically.",
    {2: ("Gives three concrete benefits (managing library dependencies including transitive ones, running tests automatically, packaging a jar, a standard layout and repeatable builds) and says the POM is a shared description so every machine builds the same way.",
         ["Maven downloads the libraries and the libraries they depend on, so I don't copy jars around. It runs the tests as a step of the build. It packages the compiled code into a jar. The pom.xml describes all of that in one shared file, so every developer's machine and the build server build the project the same way.",
          "It manages dependencies, runs the tests, and produces the jar, all from a standard layout. The POM is the one description everyone shares, so builds are repeatable."]),
     1: ("Gives one or two benefits, or says it's easier without saying how.",
         ["It downloads libraries.", "It's easier."]),
     0: ("Incorrect, for example says Maven makes the Java code run faster, or that javac can't compile packages.",
         ["Maven makes the code run faster.", "javac can't compile more than one file."])})
reg({"j4-l2.1": ("Maven: project layout and the POM", ["J4.03"])},
    {"MC136": (["J4.03"], "I67", "Tests can live in src/main/java and still be run by Maven"),
     "MC137": (["J4.03"], "Platform", "The target directory should be committed to version control"),
     "MC138": (["J4.03"], "I66", "A testing library doesn't need a test scope")})

# ====================================================================== 4.2.2
Lesson("j4-l2.2", "Maven: lifecycle, dependencies and conflicts", ["J4.04"], [
    ("o1", "Explain the build lifecycle: running a phase runs the earlier phases first, and a failure stops the build"),
    ("o2", "Read Maven's output for a passing and a failing test"),
    ("o3", "Read a dependency tree, and explain a version conflict and how Maven chooses a version"),
], ["j4-l2.1"], 55, ["I65", "I66", "I68", "R16"], r'''
## Before you start

You should be able to read a POM ([Maven: project layout and the POM](j4-l2.1)).

**Quick check.** What does `<scope>test</scope>` do?

<details><summary>Show the answer</summary>

It makes the dependency available only for compiling and running tests.

</details>
''' + NOTE + r'''
## Explanation

### The build lifecycle

Maven builds by running **phases** in a fixed order. The default lifecycle has, among others `[I65]`:

| Phase | What it does |
|---|---|
| `validate` | checks the project is correct and has the information it needs |
| `compile` | compiles the source code |
| `test` | runs the unit tests against the compiled code |
| `package` | packages the compiled code, for example into a JAR |
| `verify` | runs any checks on the results, such as integration tests |
| `install` | puts the package into your local repository, for use by other local projects |
| `deploy` | copies the package to a remote repository for sharing |

When you run one phase, Maven runs **every phase before it too**. Here is `mvn package` on my project, trimmed to the steps and results:

```
$ mvn package
[INFO] --- resources:3.5.0:resources (default-resources) @ shop ---
[INFO] --- compiler:3.16.0:compile (default-compile) @ shop ---
[INFO] --- resources:3.5.0:testResources (default-testResources) @ shop ---
[INFO] --- compiler:3.16.0:testCompile (default-testCompile) @ shop ---
[INFO] --- surefire:3.5.6:test (default-test) @ shop ---
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.020 s -- in com.example.shop.PriceTest
[INFO] Tests run: 4, Failures: 0, Errors: 0, Skipped: 0
[INFO] --- jar:3.5.1:jar (default-jar) @ shop ---
[INFO] Building jar: .../shop/target/shop-1.0-SNAPSHOT.jar
[INFO] BUILD SUCCESS
```

Each `--- plugin:version:goal ---` line is a step. Asking for `package` compiled the main code, compiled the tests, **ran the tests**, and only then built the jar. A **goal** is a task a plugin performs; a phase is a slot in the lifecycle that several goals attach to.

`mvn test` stops after the tests. `mvn clean` is a separate lifecycle that deletes `target`, and `mvn clean package` does both.

### A failing test stops the build

I changed the tax rate in `Price.java` from 20% to 25% without updating the tests, and ran `mvn package` again:

```
[INFO] --- surefire:3.5.6:test (default-test) @ shop ---
[ERROR] Tests run: 4, Failures: 1, Errors: 0, Skipped: 0, Time elapsed: 0.023 s <<< FAILURE! -- in com.example.shop.PriceTest
[ERROR] com.example.shop.PriceTest.addsTwentyPercent -- Time elapsed: 0.003 s <<< FAILURE!
org.opentest4j.AssertionFailedError: expected: <1200> but was: <1250>
	at org.junit.jupiter.api.Assertions.assertEquals(Assertions.java:569)
	at com.example.shop.PriceTest.addsTwentyPercent(PriceTest.java:12)

[ERROR] Failures: 
[ERROR]   PriceTest.addsTwentyPercent:12 expected: <1200> but was: <1250>
[ERROR] Tests run: 4, Failures: 1, Errors: 0, Skipped: 0
[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:3.5.6:test (default-test) on project shop: There are test failures.
```

Read it from the top:

- **`Tests run: 4, Failures: 1`**: four tests ran, one failed.
- **Which test:** `PriceTest.addsTwentyPercent`, and the line of the test: `PriceTest.java:12`.
- **Why:** `expected: <1200> but was: <1250>`. JUnit's `assertEquals(expected, actual)` takes the expected value **first** `[I68]`, so 1200 is what the test wanted and 1250 is what the code returned.
- **What it means for the build:** the failure happened in the `test` phase, so the `jar` step **never ran**. No jar was created in `target`. A failing test stops the pipeline: that's the point of running tests in the build.

When there is a failure, the lines to read are the first `FAILURE` line and the `expected ... but was ...` message, not the pages of Maven advice at the end.

### What a test looks like

For reference, the four tests were written like this. (Test-writing is the subject of the next module.)

```java
class PriceTest {

    @Test
    void addsTwentyPercent() {
        assertEquals(1200, Price.withTax(1000));
    }

    @Test
    void rejectsNegativePrices() {
        assertThrows(IllegalArgumentException.class, () -> Price.withTax(-1));
    }
}
```

JUnit test classes and methods needn't be `public`, but must not be `private` `[I68]`. A `@Test` method passes unless it throws, and the assertions are what throw.

### Dependencies bring dependencies

A library you add usually depends on other libraries, and those on others. Maven fetches them all, which is a huge convenience and a source of trouble. `mvn dependency:tree` prints the whole tree. For my project with only JUnit:

```
$ mvn dependency:tree
[INFO] com.example:shop:jar:1.0-SNAPSHOT
[INFO] \- org.junit.jupiter:junit-jupiter:jar:6.1.3:test
```

(With `-Dverbose` it also lists the libraries `junit-jupiter` itself pulls in, such as `junit-jupiter-api` and `junit-jupiter-engine`.)

### Version conflicts

Suppose two libraries need **different versions of the same third library**. Only one version can be on the classpath. Maven decides by **dependency mediation**: it picks the **nearest definition**, the version closest to your project in the tree, and you can always guarantee a version by declaring it explicitly in your POM `[I66]`.

I added `commons-text` 1.11.0 to the project, which itself depends on `commons-lang3`. Without anything else, the tree shows what it brings:

```
[INFO] \- org.apache.commons:commons-text:jar:1.11.0:compile
[INFO]    \- org.apache.commons:commons-lang3:jar:3.13.0:compile
```

Then I also declared `commons-lang3` **directly** at an older version, 3.9. The verbose tree now shows the conflict:

```
[INFO] +- org.apache.commons:commons-text:jar:1.11.0:compile
[INFO] |  \- (org.apache.commons:commons-lang3:jar:3.13.0:compile - omitted for conflict with 3.9)
[INFO] \- org.apache.commons:commons-lang3:jar:3.9:compile
```

Read it: `commons-text` wanted `commons-lang3` 3.13.0, but Maven **omitted it for conflict with 3.9**, because the direct declaration is nearer. The project now runs with **3.9**, a version `commons-text` was never built against. That can fail at run time, with errors such as `NoSuchMethodError`, if `commons-text` calls something that 3.9 doesn't have. Compilation won't warn you.

Fixes, in order of preference:

1. **Don't declare it directly** unless you use it yourself; let Maven use the version the library wants (3.13.0, as the first tree showed).
2. **Declare the newer version explicitly** if you do need it, so everyone uses one agreed version.
3. **Exclude** a dependency or use dependency management for bigger projects.

Always read `dependency:tree` when something behaves oddly after adding or upgrading a library.

## Worked examples

### Example 1: why was there no jar?

*Task: `mvn package` printed `BUILD FAILURE` and there's no jar in `target`. Why?*

**Step 1 — Find the failing step:** the `surefire:test` line shows `Failures: 1`.

**Step 2 — The lifecycle order:** `test` comes before `package`, and a failure stops the build.

**Step 3 — Fix the cause:** make the test and the code agree, and run again.

### Example 2: which version runs?

*Task: your POM declares `commons-lang3` 3.9 and `commons-text` 1.11.0 (which wants 3.13.0). Which version of `commons-lang3` runs?*

**Step 1 — Where is each declaration?** 3.9 is a direct dependency; 3.13.0 is one level down, under `commons-text`.

**Step 2 — Nearest wins:** `[I66]` the direct declaration is nearer.

**Step 3 — Answer:** 3.9. The tree says so: `omitted for conflict with 3.9`.

## Where this is used

- **Continuous integration** runs `mvn verify` (or similar) on every push, and a failing test stops the pipeline.
- **Upgrading libraries** means reading dependency trees and resolving conflicts.
- **Security fixes** often mean forcing a newer version of a library buried in the tree.

## Common mistakes

:::mistake{id=MC139}
**Reading the end of Maven's output first.** The useful lines are the first `FAILURE` line and the `expected ... but was` message. The generic advice after them rarely helps.
:::

:::mistake{id=MC140}
**Assuming a failed test still leaves a jar.** A failure in `test` stops the lifecycle before `package`.
:::

:::mistake{id=MC141}
**Declaring a library you don't use, at a different version from the one your other libraries need.** It overrides what they asked for and can break them at run time.
:::

## Practice

::exercise{id=j4-l2.2-explain-lifecycle}

::exercise{id=j4-l2.2-explain-failure}

::exercise{id=j4-l2.2-explain-conflict}

## Further reading

- **Maven, "Introduction to the Build Lifecycle"** `[I65]` lists the phases.
- **Maven, "Introduction to the Dependency Mechanism"** `[I66]` explains mediation, scope and exclusions.
- **JUnit User Guide, "Writing Tests"** `[I68]` for assertions and test method rules.
- **McCauley et al. (2008)** `[R16]` on debugging: an `expected ... but was` message is a ready-made hypothesis to test.

## How you'll be assessed

- The **explain** exercises check that you can describe the lifecycle, read a failing build, and explain a version conflict (*explanation*).
''' + FOOT)

ex = Exercises("j4-l2.2")
ex.explain("j4-l2.2-explain-lifecycle", "What ran, and in what order?", ["o1"], ["J4.04"],
    "You run `mvn package` and see these steps:\n\n```\n--- resources:3.5.0:resources ---\n--- compiler:3.16.0:compile ---\n--- resources:3.5.0:testResources ---\n--- compiler:3.16.0:testCompile ---\n--- surefire:3.5.6:test ---\n--- jar:3.5.1:jar ---\nBUILD SUCCESS\n```\n\n(a) You asked for `package`. Why did tests run, and why before the jar? (b) If the surefire step had reported a failing test, what would have happened to the `jar` step, and why? (c) What does `mvn test` do differently from `mvn package`?",
    "A full answer says running a phase runs all earlier phases in the lifecycle (compile, test, then package), so the tests ran as part of reaching package and before the jar; a failing test stops the build so the jar step would not run and no jar would be made; and mvn test stops after the test phase without packaging.",
    {2: ("Says Maven runs every earlier phase before the requested one so compile and test come before package, says a failing test stops the build so the jar step doesn't run, and says mvn test stops after the test phase.",
         ["Maven runs all the phases before the one you ask for, in order: compile, test, then package. So the tests ran on the way and before the jar. If a test had failed, the build would have stopped there and the jar step would never have run, so there'd be no jar. mvn test stops after the test phase and doesn't package.",
          "(a) Requesting package runs everything earlier, including test. (b) The jar step wouldn't run: a failure stops the build. (c) mvn test stops at the tests."]),
     1: ("Answers one or two parts, or says the right things without the reason.",
         ["Test runs before package.", "The jar wouldn't be made."]),
     0: ("Incorrect, for example says the jar is built first, or that failing tests are ignored.",
         ["The jar is built before the tests.", "Failing tests don't affect the build."])})
ex.explain("j4-l2.2-explain-failure", "Read the failure", ["o2"], ["J4.04"],
    "Maven prints:\n\n```\n[ERROR] Tests run: 4, Failures: 1, Errors: 0, Skipped: 0 ... <<< FAILURE! -- in com.example.shop.PriceTest\n[ERROR] com.example.shop.PriceTest.addsTwentyPercent ... <<< FAILURE!\norg.opentest4j.AssertionFailedError: expected: <1200> but was: <1250>\n\tat com.example.shop.PriceTest.addsTwentyPercent(PriceTest.java:12)\n```\n\nand the test is `assertEquals(1200, Price.withTax(1000));`. (a) How many tests ran and how many failed? Which one failed, and where? (b) What was the expected value, and what did the code return? Which argument of `assertEquals` is which? (c) Give two possible causes and say how you'd decide which is right.",
    "A full answer says four tests ran and one failed, addsTwentyPercent at PriceTest.java line 12; the expected value was 1200 and the code returned 1250, and in assertEquals the first argument is the expected value and the second the actual; and the cause is either the code (the tax rate changed to 25%) or the test (still expecting 20%), decided by going back to the requirement.",
    {2: ("Says 4 ran and 1 failed (addsTwentyPercent, PriceTest.java:12), expected 1200 and actual 1250 with expected as the first assertEquals argument, and names the code or the test as the possible fault decided by checking the requirement.",
         ["Four tests ran and one failed: addsTwentyPercent, at line 12 of PriceTest.java. It expected 1200 but the code returned 1250; in assertEquals the first argument is the expected value and the second is the actual value. Either the code is wrong (maybe the tax rate was changed to 25%) or the test is out of date; I'd go back to the requirement to decide which is right.",
          "4 tests, 1 failure: addsTwentyPercent (PriceTest.java:12). Expected 1200, got 1250 (expected comes first). The bug might be in Price (rate now 25%) or the test might be stale; check what the rule should be."]),
     1: ("Answers some parts, for example which test failed and the values but not the causes or argument order.",
         ["addsTwentyPercent failed.", "It expected 1200 and got 1250."]),
     0: ("Incorrect, for example reads the values the wrong way round, or says the build tool is broken.",
         ["Maven is broken.", "It expected 1250 and got 1200."])})
ex.explain("j4-l2.2-explain-conflict", "Which version runs?", ["o3"], ["J4.04"],
    "The verbose dependency tree of a project shows:\n\n```\n+- org.apache.commons:commons-text:jar:1.11.0:compile\n|  \\- (org.apache.commons:commons-lang3:jar:3.13.0:compile - omitted for conflict with 3.9)\n\\- org.apache.commons:commons-lang3:jar:3.9:compile\n```\n\n(a) Which version of `commons-lang3` will the project use, and why? (b) What is the risk to `commons-text`? (c) Give two ways to remove the problem, and say how you would check that it's gone.",
    "A full answer says the project will use 3.9 because Maven picks the nearest definition and the direct declaration is nearer than the one under commons-text; the risk is that commons-text was built for 3.13.0 and may call things 3.9 lacks, failing at run time (for example NoSuchMethodError); and fixes are to remove the direct declaration (so 3.13.0 is used) or declare the newer version explicitly, checking with mvn dependency:tree.",
    {2: ("Says 3.9 is used because Maven picks the nearest definition and the direct declaration is nearer, says commons-text expects 3.13.0 so could fail at run time, and gives two fixes (remove the direct declaration or declare the newer version) checked with dependency:tree.",
         ["It uses 3.9: Maven chooses the nearest definition, and the direct declaration is nearer than the 3.13.0 under commons-text. The risk is that commons-text was built against 3.13.0 and might call methods that 3.9 doesn't have, so it could fail at run time, perhaps with NoSuchMethodError. I could remove my direct declaration so 3.13.0 is used, or declare 3.13.0 or newer myself. I'd check by running mvn dependency:tree again and looking at which version is used.",
          "(a) 3.9, since the direct dependency is nearest. (b) commons-text may need features from 3.13.0 and break at run time. (c) Remove the direct 3.9 or change it to the newer version, then check the tree."]),
     1: ("Answers one or two parts, for example the version but not the reason or the risk.",
         ["It uses 3.9.", "Remove the dependency."]),
     0: ("Incorrect, for example says the newest version is always chosen, or that there is no risk.",
         ["Maven always picks the newest version.", "There's no problem as it still compiles."])})
reg({"j4-l2.2": ("Maven: lifecycle, dependencies and conflicts", ["J4.04"])},
    {"MC139": (["J4.04"], "R16", "The generic advice at the end of Maven's output is the part to read first"),
     "MC140": (["J4.04"], "I65", "A jar is still built when a test fails"),
     "MC141": (["J4.04"], "I66", "Declaring a library at a different version than another library needs is harmless")})
print("4.1 and 4.2 written")
