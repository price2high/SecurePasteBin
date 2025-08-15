# Troubleshooting

### PowerShell says the script is not recognized
- You’re not in the folder that contains it, or execution policy is blocking it.
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\make_release.ps1
```

### Inno Setup not found
- Install from https://jrsoftware.org/isdl.php and re-run:
```powershell
.\make_release.ps1 -InnoSetup "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

### `InvalidToken` during decrypt
- Role or base key doesn’t match the sender’s.
- Blob corrupted during copy/paste (try using a `.spaste` file).

### `ModuleNotFoundError: tkinter`
- Re-run the Python installer and ensure **tcl/tk** feature is selected.

### App launches but no icon / old icon
- Windows icon cache may need refresh. Rebuild EXE and installer, re-install.
