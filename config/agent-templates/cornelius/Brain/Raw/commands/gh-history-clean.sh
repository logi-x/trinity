cd ~
rm -rf experts-clean.git
git clone git@github.com:logi-x/experts.git experts-clean.git
cd experts-clean.git

git config --unset remote.origin.mirror || true

git filter-repo --force \
  --path apps/experts-app/app/api/v1/commerce/invoices/[id]/pdf/issue-fix.md \
  --path apps/experts-app/app/api/v1/commerce/invoices/[id]/pdf/queue.txt \
  --invert-paths

git filter-repo --force \
  --path miscellaneous/ \
  --path extra/ \
  --path extras/ \
  --path graphify-out/ \
  --path apps/experts-app/graphify-out/ \
  --invert-paths

cat >> .gitignore <<'EOF'
# Removed assets
# Moved to CDN / removed public assets
graphify-out/
apps/experts-app/graphify-out/
miscellaneous/
extra/
extras/

EOF

git add .gitignore
git commit -m "chore: ignore removed public assets"

git gc --prune=now --aggressive
git count-objects -vH

git rev-list --objects --all \
| git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
| sed -n 's/^blob //p' \
| sort -k2nr \
| head -30

git remote add origin git@github.com:logi-x/experts.git 2>/dev/null || true
git push origin --force --all
git push origin --force --tags

# reset to main
git fetch origin --prune
git tag -l | xargs -r git tag -d
git fetch origin --tags --force
git reset --hard origin/main
git clean -fd

# v2
git fetch origin --prune --tags
git reset --hard origin/main
git clean -fdx

# check status

git status -sb
git rev-list --left-right --count origin/main...HEAD
git rev-list --left-right --count @{u}...HEAD