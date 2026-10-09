#!/bin/sh
set -eu

export DEBIAN_FRONTEND=noninteractive

# Protect essential MarkOS packages from autoremove
apt-mark manual sudo rsync

# Remove live environment and installer packages
# without running autoremove
apt-get remove --purge -y \
  live-boot \
  live-boot-doc \
  live-config \
  live-config-doc \
  live-config-systemd \
  live-tools \
  live-task-localisation \
  live-task-recommended \
  calamares \
  calamares-settings-debian

# Remove installer launcher from installed system
rm -f /usr/share/applications/io.markos.Installer.desktop
