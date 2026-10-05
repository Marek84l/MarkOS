# MarkOS

**A Debian-based Linux distribution focused on a polished, practical and ready-to-use desktop experience.**

> 🚧 **Status: Early Development**  
> MarkOS is currently under active development and is not yet recommended as a production daily-driver operating system.

## About MarkOS

MarkOS is a personal Linux distribution built on **Debian Testing**, with **GNOME** as its primary desktop environment.

The goal is to combine the flexibility and reliability of Debian with a carefully configured desktop that works well out of the box, while still giving users control over their system.

MarkOS is being developed incrementally, with every major change tested in a Live ISO and tracked in Git.

## MarkOS 0.1

The current development build includes:

- Debian Testing base
- GNOME desktop
- Bootable Live ISO
- Custom MarkOS system identity
- MarkOS Cosmic desktop experience
- Dash to Dock with custom defaults
- Dark appearance by default
- Custom MarkOS wallpapers
- Brave as the default web browser
- Flatpak and Flathub enabled
- GNOME Software
- LibreOffice
- VLC
- Resources system monitor
- Git and htop
- JetBrains Mono
- GNOME Sushi file previews
- Multimedia codecs
- CUPS printing support
- Broad firmware and hardware support

## MarkOS Appearance

Four visual styles are planned:

- **Cosmic** — dark / purple
- **Midnight** — dark / blue
- **Aurora** — dark / teal
- **Dawn** — light / orange

A dedicated **MarkOS Appearance** application is planned to allow switching the complete desktop style with a single action.

## Desktop environments

The planned desktop editions are:

- **GNOME** — primary MarkOS desktop
- **Cinnamon** — planned
- **i3** — planned

Development currently focuses exclusively on the GNOME edition.

## Building MarkOS

MarkOS uses Debian `live-build` inside a Podman build environment.

Requirements on the host:

- Linux
- Git
- Podman
- sudo

Clone the repository and build the builder image:

```bash
sudo podman build -t markos-builder -f build/Containerfile .
