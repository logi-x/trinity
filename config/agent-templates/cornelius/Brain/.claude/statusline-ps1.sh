#!/usr/bin/env bash

# Discard any JSON payload sent on stdin
while read -r _; do :; done

# Output a prompt that mirrors your PS1, with colour codes and shell expansions.
printf '%b' \
  "${debian_chroot:+($debian_chroot)}" \
  "\e[01;32m$(whoami)@$(hostname -s)\e[0m:" \
  "\e[01;34m$(pwd)\e[0m "
