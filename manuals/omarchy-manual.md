# Omarchy — The Quick Manual

*A condensed field guide to Omarchy, DHH's omakase Linux distro (Arch + Hyprland + Quickshell). Pulled from omarchy.org/manual with Miles's added notes.*

---

## What Omarchy is

- An **omakase** Linux: a complete, opinionated system — Arch base, Hyprland tiling WM, Quickshell desktop kit.
- Ships preloaded with everything a "modern, savvy" user needs: Neovim, Chromium, Obsidian, LibreOffice, Kdenlive, OBS, even a Winamp-style music player.
- Design philosophy: "zero bloat, just everything I use." Beautiful system = motivating system = productive system.

**Miles's note:** This is NOT a beginner-friendly distro. It's keyboard-first, TUI-heavy, and config-file-driven. Expect a real learning curve — but that's the point.

---

## Installation

1. Download the ISO, flash to USB (balenaEtcher on Mac/Win, caligula on Linux).
2. **Turn off Secure Boot and/or TPM in BIOS** — mandatory, they're Windows/MS schemes.
3. Boot the stick, answer config questions.
4. Choose **full-disk** (wipes drive) or **free-space** (dual boot).
5. Installs in 1–5 minutes, default **full-disk encryption (LUKS)**.

### Critical gotchas
- **Use a wired or 2.4GHz keyboard.** Full-disk encryption can't accept a Bluetooth keyboard password at boot (same reason you can't use BT in BIOS).
- **Dual boot = turn off BitLocker first** in Windows.
- **Installing for someone else:** Ctrl+C on the very first screen (keyboard selection) → "prepare for another owner." Personal setup defers to first boot; their password becomes the encryption password.
- **No-encryption install:** Ctrl+C on the disk-formatting confirmation.
- **Unattended install:** config on a second drive, for VMs/fleet machines.

**Miles's note:** Take a backup before full-disk install — it *wipes* the selected drive. This is the #1 way people lose data.

---

## The ONE hotkey to memorize: Super + K

Shows **all** keybindings. Tmux bindings: Super+Alt+K. Herdr (agent manager): Super+Ctrl+K.

**Super** = Windows key (or Cmd on a Mac keyboard).

---

## Navigation (the essentials)

| You want | Hotkey |
|---|---|
| Omarchy menu (everything) | **Super + Space** |
| Apps-only menu | Super + Alt + Space |
| System menu (suspend/restart) | Super + Escape |
| Terminal | **Super + Return** |
| Tmux terminal | Super + Alt + Return |
| Browser | Super + Shift + Return |
| File manager | Super + Shift + F |
| Editor (Neovim) | Super + Shift + N |
| Close window | **Super + W** |
| Full screen | Super + F |
| Tile/float toggle | Super + T |
| Jump to workspace 1–4 | Super + 1/2/3/4 |
| Move window to workspace | Super + Shift + 1/2/3/4 |
| Focus a direction | Super + Arrow |
| Swap windows | Super + Shift + Arrow |
| Stack vs side-by-side | Super + J |
| Dwindle ↔ scrolling layout | Super + L |
| Group windows | Super + G |
| Lock computer | Super + Ctrl + L |

**Miles's note:** The biggest mindshift — you do NOT drag or snap windows. Open a window = full screen. Open a second = they split. No overlapping, no fishing windows out from under each other.

---

## Copy / Paste (unified — works everywhere incl. terminal)

| Action | Hotkey |
|---|---|
| Copy | Super + C |
| Cut | Super + X |
| Paste | Super + V |
| Clipboard history (incl. images) | Super + Ctrl + V |

No more Ctrl+Shift+C in terminal vs Ctrl+C elsewhere. One reflex.

---

## Launching apps (direct bindings)

| App | Hotkey |
|---|---|
| Music (Spotify) | Super + Shift + M |
| Email (HEY) | Super + Shift + E |
| Calendar (HEY) | Super + Shift + C |
| AI (ChatGPT) | Super + Shift + A |
| AI (Grok) | Super + Shift + Alt + A |
| Messenger (Signal) | Super + Shift + G |
| WhatsApp | Super + Shift + Alt + G |
| Obsidian | Super + Shift + O |
| Docker (LazyDocker) | Super + Shift + D |
| X | Super + Shift + X |
| YouTube | Super + Shift + Y |
| Password manager | Super + Shift + / |

Change/add bindings in `~/.config/hypr/bindings.lua`.

---

## System controls

| Panel | Hotkey |
|---|---|
| Audio | Super + Ctrl + A |
| Bluetooth | Super + Ctrl + B |
| Wifi/network | Super + Ctrl + W |
| Display | Super + Ctrl + D |
| Power | Super + Ctrl + P |
| Activity (btop) | Super + Ctrl + T |
| Screenshot/recording | Super + Ctrl + C |
| Emoji picker | Super + Ctrl + E |
| Calculator | Super + Ctrl + Q |
| Pick AI agent | Super + Shift + Ctrl + A |

---

## Capture

| Action | Hotkey |
|---|---|
| Screenshot | Print Screen |
| Screen record | Alt + Print Screen |
| Color picker | Super + Print Screen |
| OCR text extract | Super + Ctrl + Print Screen |
| Copy URL (webapp/Chromium) | Alt + Shift + L |
| Download video to ~/Videos | Alt + Shift + D |
| Dictation | Super + Ctrl + X (or F9 push-to-talk) |

---

## Terminal & Tmux

- Default terminal: **Foot** (fast, no native tabs/splits). Alacritty/Ghostty/Kitty available via Install > Terminal.
- **Tmux** prefix key = **Ctrl + Space** (then `s` to list sessions).
- **Layout functions:**
  - `tdl [agent]` — 3-way split: editor + AI agent + terminal (`tdl c` = opencode).
  - `tds` — 4-way square.
  - `tdlm` — layout for every subdirectory.
  - `tsl [panes] [cmd]` — swarm of agents (`tsl 4 c` = 4 opencode agents).

**Miles's note:** If you work with AI coding agents, `tdl` is your new best friend — editor + agent side-by-side in one command.

---

## Neovim (omarchy-nvim, built on LazyVim)

- Leader key = **Space**.
- `Space Space` — fuzzy-find files
- `Space S G` — grep search
- `Space E` — toggle file tree
- `Ctrl+W W` — hop tree ↔ editor
- `Space G G` — LazyGit
- `Space B D` — close tab/buffer
- `n` (alias for nvim) opens editor in current dir; `n file.txt` for single file.
- sudo edits: `sudoedit /etc/sudoers.d/...`

**Miles's note:** New to vim? Watch ThePrimeagen's "Vim As Your Editor" series. It's a real learning curve, but the payoff is real.

---

## Updates (do NOT use pacman -Syu)

- Update via **Update > Omarchy** in the menu, or `omarchy update`.
- Omarchy installs itself as regular pacman packages. An update = latest Omarchy release + migrations + all system packages + AUR.
- A **circle-arrow icon** appears next to the clock when a release is ready.
- **Four channels:** stable (default), RC, edge, dev. Switch via `omarchy-channel-set`.
- **Firmware:** Update > Firmware (installs fwupd; may require reboot).
- **⚠️ Never run `pacman -Syu` / `yay -Syu` directly** — you'll skip snapshots, migrations, and config updates. Omarchy blocks it and points you to `omarchy update`.
- **Rollback:** restart → pick the pre-update snapshot in the boot menu. Or `omarchy reinstall` (wipes your config changes).

---

## System Snapshots (Time Machine equivalent)

- Auto-snapshot on every update. Manual: `omarchy-snapshot create`.
- Restore from the **Limine** boot loader (default since Omarchy 2.0).
- Restores root, NOT /home (won't recover deleted personal files).
- **Direct Boot** (Setup > Direct Boot) skips Limine → boots straight to decryption. Trade-off: harder to reach snapshots.

---

## Security (taken seriously)

- **Full-disk encryption (LUKS) mandatory.**
- **Firewall on by default** — blocks all inbound except port 53317 (LocalSend). SSH off until you enable Setup > Security > SSHD.
- Docker locked down via ufw-docker (no accidental exposure).
- **Two passwords:** drive-encryption + user/sudo. Change under Update > Password.
- **Reset Computer** (Setup > Reset Computer): wipe + hand machine to new owner, restores baseline snapshot.
- **Passwordless sudo:** Setup > Security > Passwordless Sudo (15-min auto-expire; `omarchy-sudo-passwordless 30` to extend).

---

## Themes

- **22 themes** (Tokyo Night, Catppuccin, Gruvbox, Nord, Rose Pine, etc.).
- Switch: Style > Theme, or `Super + Ctrl + Shift + Space`.
- Backgrounds: `Super + Ctrl + Space`.
- Each theme styles desktop, terminal, neovim, btop, Chromium, top bar, menu, lock screen.
- Custom **unlock (boot decryption)** designs too: Style > Unlock.
- Make your own: see the manual's "Making your own theme."

---

## Common tweaks

- **Round corners:** edit `~/.config/hypr/looknfeel.lua` → uncomment `rounding = 8`.
- **Remove gaps/borders:** toggle `Super + Shift + Backspace`, or permanently in `looknfeel.lua`.
- **Top bar toggle:** `Super + Shift + Space`.
- **Tray icons always visible:** right-click the tray expander arrow → pin.
- Updates may restore configs → your changes go to a `.bak` file, not lost.
- **Reset individual config:** Update > Config. **Reset everything:** `omarchy reinstall`.

---

## CLI (`omarchy`)

- `omarchy` — command center help
- `omarchy update` — update system
- `omarchy theme list` / `omarchy theme set <name>`
- `omarchy font list`
- `omarchy screenshot`
- `omarchy debug`
- Groups: agent, audio, bar, battery, bluetooth, branding, brightness, capture, channel, clipboard, cmd, config, debug, etc.
- Menu scriptable: `omarchy menu summon style.theme`, `omarchy menu toggle system`.
- Everything takes `--help`.

**Miles's note:** The CLI is gold when you have an AI agent working on your config — it exposes all the internal tooling. This is how you'd let an agent customize the system.

---

## Coming from Mac/Windows (translation table)

| Mac / Windows reflex | Omarchy |
|---|---|
| Spotlight / Raycast / Start | Super + Space |
| Cmd+C / Ctrl+C | Super + C |
| Win+V clipboard history | Super + Ctrl + V |
| Cmd+Shift+4 / Win+Shift+S | Print Screen |
| AirDrop | LocalSend (Super + Ctrl + S) |
| Time Machine (system) | Auto snapshots |
| App Store | Install in menu / `omarchy pkg add` |
| System Settings / Control Panel | Setup menu (edits config files) |
| Notification Center | Super + Shift + Alt + , |

**Key mindset shifts:**
1. **No dock, no desktop icons.** Apps launch via hotkeys or the menu.
2. **Windows place themselves** (tiling).
3. **Closing a window quits the app** (no macOS limbo).
4. **Settings = text files** in version control, not panels.

**Miles's note:** Give it **two weeks**. The muscle memory transfers fast, and once you're in, it's hard to go back to a mouse-driven desktop.

---

## Help when stuck

- Community Discord: `#omarchy-help` channel → omarchy.org/discord
- Full manual: omarchy.org/manual/

---

*Compiled by Miles for the Captain — 2026-08-24. Source: omarchy.org/manual/*
