# Build

## Dev Run
```powershell
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
python secure_pastebin_p2p.py
```

## Portable EXE
```powershell
build_exe.bat
# → dist\SecurePasteP2P.exe
```

## Windows Installer
Requires **Inno Setup 6** (`ISCC.exe` in Program Files).

```powershell
.\make_release.ps1
# or specify path:
.\make_release.ps1 -InnoSetup "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

## Code Signing (optional)
```powershell
signtool sign /a /tr http://timestamp.digicert.com /td sha256 /fd sha256 dist\SecurePasteP2P.exe
signtool sign /a /tr http://timestamp.digicert.com /td sha256 /fd sha256 output\SecurePasteP2P-Lilac-Setup.exe
```

## macOS/Linux
Build with PyInstaller on the target OS. (macOS may require codesign/notarization.)
