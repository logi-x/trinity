#!/bin/sh

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
ZATCA_SDK_HOME=/opt/zatca-sdk

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
add_ld_library_path $FFMPEG_HOME/usr/libexec
add_ld_library_path $ZATCA_SDK_HOME/Apps

export LD_LIBRARY_PATH
