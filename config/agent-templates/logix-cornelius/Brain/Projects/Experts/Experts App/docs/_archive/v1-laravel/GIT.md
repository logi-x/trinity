---
title: "🧠 Git Cheat Sheet – Monorepo Rebase + Squash Strategy"
date: "2026-04-11"
tags: ["project/experts", "docs/v1", "topic/git"]
category: "docs/experts-archived"
archived: true
updated: "2026-07-15"
---

## Links

- [[Projects/Experts/Experts App/docs]]

# 🧠 Git Cheat Sheet – Monorepo Rebase + Squash Strategy

A modern Git strategy designed for monorepos with multiple platforms (iOS, Android, Web, API) using **feature branches**, **platform-specific dev branches**, and **clean merges via squash + rebase**.

---

## 🌱 Branching Strategy

### 🚀 Permanent Branches

| Branch        | Purpose                       | Merge Strategy      |
| ------------- | ----------------------------- | ------------------- |
| `main`        | Production release            | Rebase & Merge only |
| `staging`     | QA testing before prod        | Rebase & Merge only |
| `development` | Central dev integration layer | Rebase & Merge only |

### 🔧 Platform Dev Branches

| Branch        | Purpose                 | Merge Strategy |
| ------------- | ----------------------- | -------------- |
| `android/dev` | Android development     | Squash only    |
| `ios/dev`     | iOS development         | Squash only    |
| `app/dev`     | Next.js web development | Squash only    |
| `api/dev`     | Laravel API development | Squash only    |

### 🌿 Feature Branches

| Branch              | Purpose                   | Notes           |
| ------------------- | ------------------------- | --------------- |
| `android/feature/*` | Android-specific features | Delete after PR |
| `ios/feature/*`     | iOS-specific features     | Delete after PR |
| `api/feature/*`     | API-specific features     | Delete after PR |
| `app/feature/*`     | Web-specific features     | Delete after PR |

---

## 🛠️ Workflow Examples

### ✅ Creating a New Feature Branch

```bash
git checkout -b android/feature/login android/dev
```

Make changes, then:

```bash
git add .
git commit -m "Add login screen"
git push -u origin android/feature/login
```

Open a pull request:
➡️ android/feature/login → android/dev
✅ Merge using: Squash & Merge
🗑 Delete the feature branch after merge

## 🔄 Rebasing Before Merging Dev Branches Upstream

### 🔁 Example: Rebasing android/dev onto development

```bash
git checkout android/dev
git fetch origin
git rebase origin/development
```

Open PR:
➡️ android/dev → development
✅ Merge using: Rebase & Merge

Repeat for:

`development → staging`

`staging → main`

### 🧼 Post-Merge: Sync Dev Branch With Upstream

After squash or rebase merging a dev branch into development, sync it back down:

```bash
git checkout android/dev
git fetch origin
git reset --hard origin/development
git push --force-with-lease
```

> ⚠️ This wipes local history of android/dev and makes it identical to development.

### 🔧 GitHub Branch Protection Rules

✅ Enable on main, staging, development

| Setting                | Value                 |
| ---------------------- | --------------------- |
| Require pull request   | ✅ Yes                |
| Require status checks  | ✅ Yes                |
| Require linear history | ✅ Yes (rebased only) |
| Allowed merge types    | ✅ Rebase & Merge     |

✅ For Platform Dev Branches

| Setting                | Value                  |
| ---------------------- | ---------------------- |
| Require pull request   | ✅ Yes                 |
| Allowed merge types    | ✅ Squash & Merge only |
| Require linear history | ❌ No                  |

### 🧠 Rebase vs Merge (Quick Guide)

| Action           | Result                                  | Use When                      |
| ---------------- | --------------------------------------- | ----------------------------- |
| git merge        | Combines commits + creates merge commit | You don’t care about history  |
| git rebase       | Rewrites commits to sit on top          | You want clean linear history |
| git reset --hard | Force a branch to match another         | After squash/rebase merges    |

### 🔁 Interactive Rebase (To Clean History)

To clean up commit history before merging a feature branch, use interactive rebase:

```bash
git rebase -i origin/android/dev
```

pick → keep commit

squash → combine commit into previous

drop → delete commit

## 🧹 Cleaning Up

After merging, delete the feature branch:

```bash
git branch -d android/feature/login
git push origin --delete android/feature/login
```

### 🔁 IDE specific rebase/sync

```bash
git checkout development
git fetch origin
git pull --rebase origin development
```

### 🧩 Setting Upstream Branches

To sync your local dev branch with the remote:

```bash
git checkout -b android/dev origin/android/dev
git branch --set-upstream-to=origin/android/dev android/dev
```

### 🔁 Renaming a Branch Safely

To rename a branch safely, use:

```bash
# 1. Switch to the branch you want to rename
git checkout web/dev
# 2. Rename the branch locally
git branch -m app/dev
# 3. Push the renamed branch to the remote
git push origin app/dev
# 4. Delete the old remote branch
git push origin --delete web/dev
# 5. Reset upstream tracking
git branch --unset-upstream
git branch --set-upstream-to=origin/app/dev app/dev
# 🧼 6. (Optional) Clean up local web/dev references
# If you’ve renamed everything, remove any old local tags, worktrees, etc., using:
git remote prune origin
```

> This renames the branch locally and on the remote, and sets the upstream tracking branch.

### 🧪 Simulating Rebase by Force-Sync

To simulate a rebase, you can force-sync your branch with the upstream branch:

```bash
git fetch origin
git reset --hard origin/development
git push --force-with-lease
```

> This does not rebase, but resets your branch to exactly match development. Useful after squash merges.

### 📌 Misc Tips

- 🔥 Always rebase feature branches before merging
- 🧹 Always delete feature branches after squash merge
- 🔁 Never merge development into a dev branch — always rebase onto it
- 👥 Ready for team scaling: this strategy keeps history clean & conflicts rare

> ✨ Structured for growth. Clean for CI. Ready for teams.

## 🧩 Summary

- **Feature branches** are used for development and deleted after merging.
- **Platform dev branches** are used for integration and rebased onto the main development branch.
- **Permanent branches** are used for production and staging releases.
- **Squash & Merge** is used for feature branches to keep history clean.
- **Rebase & Merge** is used for dev branches to keep the commit history linear.
- **Delete feature branches** after merging to keep the repository clean.
- **Use descriptive commit messages** for clarity.
- **Use pull requests** for code reviews and discussions.
- **Use tags** for marking releases in the main branch.
- **Use CI/CD** for automated testing and deployment.
- **Use Git hooks** for pre-commit checks and linting.
- **Use Git aliases** for common commands to speed up your workflow.
- **Use Git stash** for temporary changes to avoid committing unfinished work.
- **Use Git cherry-pick** for applying specific commits to other branches.
- **Use Git bisect** for debugging and finding the commit that introduced a bug.
- **Use Git reflog** for recovering lost commits and branches.
- **Use Git submodules** for managing dependencies and external repositories.
- **Use Git sparse-checkout** for checking out only specific directories in a large repository.
- **Use Git worktrees** for working on multiple branches simultaneously.
- **Use Git hooks** for automating tasks like running tests or linting before commits.
- **Use Git blame** for tracking changes and authorship of specific lines in a file.
- **Use Git log** for viewing commit history and changes.
- **Use Git diff** for comparing changes between commits, branches, or working directory.
- **Use Git status** for checking the status of your working directory and staging area.
- **Use Git config** for configuring user information and repository settings.
- **Use Git remote** for managing remote repositories and their URLs.
- **Use Git fetch** for downloading changes from remote without merging.
- **Use Git pull** for fetching and merging changes from remote.
- **Use Git push** for uploading local changes to remote.
- **Use Git clone** for creating a local copy of a remote repository.
- **Use Git init** for creating a new Git repository.
- **Use Git add** for staging changes for commit.
- **Use Git commit** for creating a new commit with staged changes.
- **Use Git reset** for undoing changes and moving the HEAD pointer.
- **Use Git checkout** for switching branches or restoring files.
- **Use Git merge** for combining changes from different branches.
- **Use Git rebase** for applying commits from one branch onto another.

### Usful Commands

```bash
git config --global user.name "Your Name"
git config --global user.email "email"

git update-index --chmod=+x --add ./scripts/pr-cleanup.sh

git rm --cached -r .
find . -maxdepth 3 -name "*.sh"
find . -maxdepth 3 -name "*.sh" -exec chmod +x {} \;
find . -maxdepth 3 -name "*.sh" -exec git update-index --chmod=+x --add {} \;

chmod +x g dkr apps/experts-api/artisan
git update-index --chmod=+x --add g dkr apps/experts-api/artisan
```

### Git Aliases

```.gitconfig
<!-- ~/.gitconfig -->
[alias]
        resync = "!f() { git fetch origin && git reset --hard origin/$1 && git push --force-with-lease; }; f"
        sync = !"git fetch origin && git merge"
        cleanup = !"git branch --merged | grep -v '\\*' | xargs -n 1 git branch -d"
        lg = log --oneline --graph --decorate --all
        s = status -sb
        last = log -1 HEAD
        cleanfetch = fetch --all --prune
        st = status
        co = checkout
        ci = commit
        br = branch
        df = diff
```

### Custom Git Scripts

```bash
📦 g — Git branch sync, cleanup, and rebase utility

USAGE:
  g [COMMAND] [OPTIONS]

COMMANDS:
  --all                 Sync all platform/dev branches with remote
  --all-dev             Rebase all platform/dev branches onto origin/development
  --pull                Pull all remote branches
  --mainflow            Sync main branches: development → staging → main
  --clean               Remove stale remote and local branches (excluding main)
  --prune               Prune stale remote branches only
  --reset <branch> [remote/base]
                        Reset a PR branch to match base (default: origin/api/dev) and force-push
  --tag <platform>      Tag current commit with platform and timestamp
  --interactive         Launch guided Git workflow (create, rebase, cleanup, etc)
  --help                Show this help message

EXAMPLES:
  g --all
  g --clean
  g --reset api/fix/cis origin/api/dev
  g --tag api
  g --interactive
  g

NOTES:
  - All rebases use --force-with-lease for safe syncing
  - Use --reset after squash merges to reuse PR branches
  - Running with no arguments will sync the current branch
```

### GitHub CI Actions

Auto CI will run on every PR to (main, staging and development) branchs. It will run tests, build, and deploy the application.

#### Available Workflows

- Android CI (Hybrid)
- iOS CI (Hybrid) -> will run on App Connect instead of GitHub
- Web CI (Next.js) -> will build the app and check for errors
- API CI (Laravel) -> will run api tests and check for errors
- Docker CI (Docker) -> will build and push the docker image to the registry
- Release CI (Main) -> will tag the release and push it to the main branch
- Slack CI (Slack) -> will notify the team on Slack when actions are completed successfully
