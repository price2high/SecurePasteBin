# Install

## Option A — Portable EXE (no install)
1) Download `SecurePasteP2P.exe` from the Releases page.
2) Double-click to run.

## Option B — Windows Installer (recommended for non-technical users)
1) Download `SecurePasteP2P-Lilac-Setup.exe` from Releases.
2) Run the installer → optional desktop shortcut.
3) Double-click any `*.spaste` file to open directly in the app (file association).

## Build from Source (Dev)

### Prereqs
- Windows 10/11, Python 3.10+
- (Optional) Inno Setup 6 if you want to compile the installer

### Create venv & run from source
```powershell
python -m venv venv
venv\Scripts\Activate
pip install -r .
equirements.txt
python .\secure_pastebin_p2p.py
```

### Build portable EXE
```powershell
build_exe.bat
# → dist\SecurePasteP2P.exe
```

### Build installer & release zip
```powershell
# compile EXE → installer → zip
.\make_release.ps1
# If Inno Setup is not found, pass its path:
.\make_release.ps1 -InnoSetup "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```
