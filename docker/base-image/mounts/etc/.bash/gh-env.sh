# Trinity gh auth — export GH_TOKEN so `gh` (and anything reading GH_TOKEN) is
# authenticated. Prefers a short-lived GitHub App installation token (so the
# agent authors as its App bot, e.g. agent-experts[bot]); falls back to
# GITHUB_PAT (Trinity-injected; MAY be read-only).
#
# Sourced two ways so every shell is covered:
#   - interactive shells:      .bashrc -> logix.env.sh -> here
#   - non-interactive shells:  ENV BASH_ENV=/etc/.bash/gh-env.sh (agent loops,
#                              `bash -c ...`) read this directly.
# Self-contained: gh, openssl, curl, python3 and the minter all resolve on the
# image's default PATH, so this does NOT depend on logix.env.sh's PATH edits.
#
# Per-agent config lives in the agent's .env (the App ID / Installation ID are
# not secret; the private key is injected out-of-band):
#   GH_APP_ID, GH_APP_INSTALLATION_ID, and GH_APP_PEM_B64 (or a *.pem on disk).

if [ -z "${GH_TOKEN:-}" ]; then
  # First runnable minter wins: a repo-local script (agent-specific overrides),
  # then the generic fleet minter baked into the base image.
  _ghmint=""
  for _c in "$HOME/scripts/gh-app-token.sh" "/usr/local/bin/gh-app-token" "$HOME/.trinity/gh-app-token.sh"; do
    [ -x "$_c" ] && { _ghmint="$_c"; break; }
  done
  if [ -n "$_ghmint" ]; then
    # BASH_ENV= is REQUIRED, not cosmetic: the minter is a bash script and
    # BASH_ENV points back at THIS file. Without clearing it, the minter's shell
    # (and every $(...) inside it) re-sources this while GH_TOKEN is still unset,
    # re-runs the minter, and recurses without bound → fork bomb (tens of
    # thousands of PIDs, container hits its memory cap, WSL2/Docker OOMs). Do NOT
    # remove the `BASH_ENV=` prefix.
    _ght="$(BASH_ENV= "$_ghmint" 2>/dev/null || true)"
    [ -n "$_ght" ] && export GH_TOKEN="$_ght"
  fi
  # Fall back to the injected PAT when no App token could be minted.
  [ -z "${GH_TOKEN:-}" ] && [ -n "${GITHUB_PAT:-}" ] && export GH_TOKEN="${GITHUB_PAT}"
  unset _ghmint _ght _c 2>/dev/null || true
fi
