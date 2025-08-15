# Secure Paste P2P — Lilac Princess Edition 👑✨

A tiny, friendly Windows app for **serverless** secret sharing. It encrypts locally,
outputs a compact **blob** (or QR), and only someone with the **base key + correct role**
can decrypt it — all **without a server**.

- **Peer-to-peer**: share as text/QR or `*.spaste` file
- **End-to-end**: key never leaves the sender/receiver
- **Role-bound crypto**: decryption key is derived from _base key + role + salt_
- **Cute UI**: lilac theme + optional rainbow trash-can icon 🗑️🌈

---

## Quick Start (Windows)

1. **Download & run** the installer or portable EXE (see **[Install](docs/INSTALL.md)**).
2. **Encrypt tab** → write secret → set role (e.g., `admin`) → **Create Blob**.
   - Share the **blob** (text/QR/`.spaste`) with the recipient.
   - Share the **base key** using a separate channel (phone/SMS).
3. **Decrypt tab** → paste or open blob → enter **role** + **base key** → **Decrypt**.

> Tip: Delete the blob after first delivery if you want “burn‑after‑read”.

---

## Sneak Peek
(see more in **[Screenshots](https://github.com/price2high/SecurePasteBin/blob/main/SCREENSHOTS.md)**)

![Encrypt](https://github.com/price2high/SecurePasteBin/blob/main/07-screenshot.png)
![Decrypt](https://github.com/price2high/SecurePasteBin/blob/main/06-screenshot.png)
![App Search](https://github.com/price2high/SecurePasteBin/blob/main/01-screenshot.png)

---

## Repo Layout

```
/
├─ secure_pastebin_p2p.py          # app source
├─ app.ico                         # rainbow trash can or lilac crown icon
├─ requirements.txt
├─ build_exe.bat                   # PyInstaller build (portable EXE)
├─ installer.iss                   # Inno Setup script (.spaste association)
├─ make_release.ps1                # build EXE → compile installer → zip release
├─ docs/                           # documentation + screenshots
└─ LICENSE
```

---

## Docs

- **[Install](docs/INSTALL.md)** — EXE, installer, and source build steps
- **[Usage](docs/USAGE.md)** — encrypt, decrypt, QR, file workflows
- **[Security Model](docs/SECURITY.md)** — HKDF + Fernet design, limitations
- **[Threat Model](docs/THREAT_MODEL.md)** — risks & mitigations
- **[Build](docs/BUILD.md)** — PyInstaller & Inno Setup, code signing
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** — common issues & fixes
- **[FAQ](docs/FAQ.md)** — quick answers
- **[Roadmap](docs/ROADMAP.md)** — planned enhancements
- **[Contributing](docs/CONTRIBUTING.md)**, **[Code of Conduct](docs/CODE_OF_CONDUCT.md)**
- **[Changelog](docs/CHANGELOG.md)** — 2025-08-15

---

## License

MIT — see **[LICENSE](LICENSE)**.
