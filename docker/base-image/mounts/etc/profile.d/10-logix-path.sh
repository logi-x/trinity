#!/bin/sh

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"

add_path() {
  [ -d "$1" ] && PATH="$1:$PATH"
}

PHP_HOME=/opt/php
NODE_HOME=/opt/node
JAVA_HOME=/opt/java/openjdk
CHROMIUM_HOME=/opt/chromium
PYTHON_HOME=/opt/python
GO_HOME=/opt/go
FFMPEG_HOME=/opt/ffmpeg
ZATCA_SDK_HOME=/opt/zatca-sdk

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
add_path $ZATCA_SDK_HOME/usr/bin

export PATH
