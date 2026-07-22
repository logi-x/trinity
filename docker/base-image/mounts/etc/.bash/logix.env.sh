#!/bin/sh

# ===== PATHS =====
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

add_path() {
  [ -d "$1" ] && PATH="$1:$PATH"
}

PHP_HOME=/opt/php
NODE_HOME=/opt/node
JAVA_HOME=/opt/java/openjdk
CHROMIUM_HOME=/opt/chromium
FONTS_HOME=/opt/fonts
PYTHON_HOME=/opt/python
GO_HOME=/opt/go
FFMPEG_HOME=/opt/ffmpeg
ZATCA_SDK_HOME=/opt/zatca-simulator
SDK_CONFIG=/opt/zatca-simulator/Configuration/config.json
FATOORA_HOME=/opt/zatca-simulator/Apps

add_path $NODE_HOME/usr/local/bin
add_path $JAVA_HOME/bin
add_path $CHROMIUM_HOME/bin
add_path $PHP_HOME/usr/local/bin
add_path $PHP_HOME/usr/bin
add_path $PYTHON_HOME/usr/local/bin
add_path $GO_HOME/bin
add_path $FFMPEG_HOME/usr/bin
add_path $FFMPEG_HOME/usr/libexec
add_path $ZATCA_SDK_HOME/Apps

# ===== LD_LIBRARY_PATHS =====
LD_LIBRARY_PATH="${LD_LIBRARY_PATH:-}"

add_ld_library_path() {
  [ -d "$1" ] || return

  case ":$LD_LIBRARY_PATH:" in
    *:"$1":*) ;;
    *) LD_LIBRARY_PATH="$1:$LD_LIBRARY_PATH" ;;
  esac
}

PHP_HOME=/opt/php
NODE_HOME=/opt/node
JAVA_HOME=/opt/java/openjdk
CHROMIUM_HOME=/opt/chromium
PYTHON_HOME=/opt/python
GO_HOME=/opt/go
FFMPEG_HOME=/opt/ffmpeg
ZATCA_SDK_HOME=/opt/zatca-simulator

add_ld_library_path $PHP_HOME/usr/lib
add_ld_library_path $PHP_HOME/usr/local/lib
add_ld_library_path $NODE_HOME/usr/lib
add_ld_library_path $NODE_HOME/usr/local/lib
add_ld_library_path $JAVA_HOME/lib
add_ld_library_path $CHROMIUM_HOME/lib
add_ld_library_path $CHROMIUM_HOME/lib/pulseaudio
add_ld_library_path $CHROMIUM_HOME/lib/dri
add_ld_library_path $CHROMIUM_HOME/lib/pipewire-0.3
add_ld_library_path $CHROMIUM_HOME/lib/gdk-pixbuf-2.0
add_ld_library_path $CHROMIUM_HOME/lib/gio
add_ld_library_path $CHROMIUM_HOME/lib/gtk-3.0
add_ld_library_path $PYTHON_HOME/usr/lib
add_ld_library_path $PYTHON_HOME/usr/local/lib
add_ld_library_path $FFMPEG_HOME/usr/lib
add_ld_library_path $FONTS_HOME/lib

# ===== ALIASES =====
alias pa="php artisan"
alias art="php artisan"
alias tinker="php artisan tinker"
alias cu="composer update"
alias ci="composer install"
alias cr="composer require"
alias pnpmi="pnpm install"
# list commands
alias ll="ls -alF"
alias la="ls -A"
alias l="ls -CF"
# navigation commands
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."
alias ......="cd ../../../../.."
alias cdc="cd /c"
alias cdd="cd /d"
alias app="cd /app"
# clear commands
alias c="clear"
# edit commands
alias rc="nano ~/.bashrc"
alias rc="nano ~/.bashrc"

# ===== GENERAL =====
export TERM=xterm-256color
export EDITOR=nano

# 🌐 Locale configuration
export LANG=en_US.UTF-8
export TZ=Asia/Riyadh

# 📦 Development configuration
export TURBO_TELEMETRY_DISABLED=1
export NEXT_TELEMETRY_DISABLED=1
export SDK_CONFIG=$SDK_CONFIG
export FATOORA_HOME=$FATOORA_HOME
export ZATCA_SDK_HOME=$ZATCA_SDK_HOME
export FFMPEG_HOME=$FFMPEG_HOME
export PYTHON_HOME=$PYTHON_HOME
export GO_HOME=$GO_HOME
export NODE_HOME=$NODE_HOME
export PHP_HOME=$PHP_HOME

# 📦 Chromium configuration
export CHROMIUM_HOME=$CHROMIUM_HOME
export PUPPETEER_EXECUTABLE_PATH=$PUPPETEER_EXECUTABLE_PATH
export FONTCONFIG_PATH=/opt/fonts/share/fonts
export FONTCONFIG_FILE=/opt/fonts/etc/fonts/fonts.conf
export CHROMIUM_PATH=/opt/chromium/bin/chromium-browser
export XDG_DATA_HOME=/var/.data
export XDG_CONFIG_HOME=/var/.config
export XDG_CACHE_HOME=/var/.cache
export PANGOCAIRO_BACKEND=fc
export JAVA_HOME=$JAVA_HOME

export PNPM_STORE_PATH=/var/.cache/pnpm

# Export paths
export PATH
export LD_LIBRARY_PATH
# export PATH=/opt/php/usr/local/bin:/opt/php/usr/bin:/opt/node/usr/local/bin:/opt/node/usr/bin:/opt/java/openjdk/bin:/opt/chromium/bin:/opt/ffmpeg/usr/bin:/opt/ffmpeg/usr/libexec:/opt/zatca-sdk/Apps:/opt/zatca-sdk/usr/bin:$PATH
# export PATH=$PATH

# . /etc/.bash/utils.sh

# GitHub auth for interactive shells: export GH_TOKEN (App bot token, else
# GITHUB_PAT). Non-interactive shells get this via ENV BASH_ENV=/etc/.bash/gh-env.sh.
[ -f /etc/.bash/gh-env.sh ] && . /etc/.bash/gh-env.sh
