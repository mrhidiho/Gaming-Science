# Git practice worksheet

Use a NEW disposable practice folder. Never run this against an employer or important existing repository. Run one command at a time and inspect its output. Git must be installed. Author identity is your choice; do not copy another person's details. No remote account or push is required. [S13, S16]

```sh
mkdir course-git-practice
cd course-git-practice
git init --initial-branch=main
```

When identity is missing, configure it locally for this practice repository using your chosen display name and an appropriate email/privacy choice. These example placeholders must be replaced; they are not instructions to impersonate anyone:

```sh
git config --local user.name "Your chosen commit name"
git config --local user.email "Your chosen commit email"
```

In an editor, create `rules.txt` containing `damage=3`. Save it, then inspect and commit:

```sh
git status
git add rules.txt
git diff --staged
git commit -m "Define starting damage rule"
git switch -c boundary-fix
```

Add a second line `health_min=0` in the editor, inspect and commit. Then merge:

```sh
git diff
git add rules.txt
git commit -m "Specify zero-health boundary"
git switch main
git merge --ff-only boundary-fix
```

Change damage to 30 as an intentional mistake. Commit it, then revert that last commit:

```sh
git add rules.txt
git commit -m "Demonstrate mistaken damage value"
git revert --no-edit HEAD
git log --oneline --graph --all
git status
git tag module04-reviewed
```

Check that damage is 3 and health_min is 0. Explain all four commits: baseline, boundary feature, mistake and revert. The tag marks the reviewed state, not proof that a test ran. Record commands, staged differences and final content. In a separate small experiment, stage a file then edit it again and compare `git diff` with `git diff --staged`.

The supplied `tools/git_sandbox.py` demonstrates a similar sequence in its own temporary repository and does not alter global Git configuration. It is not a replacement for explaining your own history. Do not use force-push, hard reset or broad deletion as part of this exercise.
