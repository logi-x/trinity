set -e

# --- claude settings seed -----------------------------------------------------
mkdir -p "$HOME/.claude"
cat > "$HOME/.claude/settings.json" <<'EOF'
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/stop-hook-git-check.sh"
          }
        ]
      }
    ]
  },
  "permissions": {
    "allow": [
      "Skill",
      "mcp__Linear__*",
      "mcp__Slack__*",
      "mcp__github__*"
    ]
  }
}
EOF

# --- toolchain ----------------------------------------------------------------
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
corepack enable
corepack prepare pnpm@11.0.8 --activate

# --- 1. resolve REPO_ROOT -----------------------------------------------------
REPO_ROOT=/home/user/experts
[ -d "$REPO_ROOT/apps/experts-app" ] || REPO_ROOT="$PWD"
[ -d "$REPO_ROOT/apps/experts-app" ] || REPO_ROOT="$HOME/experts"

if [ ! -d "$REPO_ROOT/apps/experts-app" ]; then
    echo "Could not locate experts repo root" >&2
    echo "Tried: /home/user/experts, \$PWD=$PWD, \$HOME/experts=$HOME/experts" >&2
    exit 1
fi

echo "Using REPO_ROOT=$REPO_ROOT"
cd "$REPO_ROOT"

# --- 2. DATABASE_URL placeholder so prisma generate can parse the schema -------
export DATABASE_URL="${DATABASE_URL:-postgresql://placeholder:placeholder@localhost:5432/placeholder}"
export SHADOW_DATABASE_URL="${SHADOW_DATABASE_URL:-postgresql://placeholder:placeholder@localhost:5432/placeholder}"

# --- 3. root pnpm install (skip if node_modules exists) -----------------------
if [ ! -d "$REPO_ROOT/node_modules" ]; then
    cd "$REPO_ROOT" && pnpm install --frozen-lockfile
else
    echo "Skipping root install — node_modules present"
fi

# --- 4. app pnpm install + prisma generate (skip install if node_modules exists)
if [ ! -d "$REPO_ROOT/apps/experts-app/node_modules" ]; then
    cd "$REPO_ROOT/apps/experts-app" && pnpm install --frozen-lockfile && pnpm db:generate
else
    echo "Skipping app install — node_modules present (running db:generate only)"
    cd "$REPO_ROOT/apps/experts-app" && pnpm db:generate
fi
