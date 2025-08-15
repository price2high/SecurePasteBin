import os
import json
import base64
import secrets
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

import qrcode
from PIL import Image, ImageTk

APP_TITLE = "Secure Paste (P2P, Lilac Princess Edition)"
BLOB_VERSION = 1

# ----------------- Helper functions -----------------
def b64u_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")

def b64u_decode(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def derive_fernet_key(base_key_b64: str, role: str, salt: bytes) -> bytes:
    base_key = b64u_decode(base_key_b64)
    info = f"secure-paste-p2p|role:{role.strip().lower()}|v:{BLOB_VERSION}".encode("utf-8")
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=info)
    derived = hkdf.derive(base_key)
    return base64.urlsafe_b64encode(derived)

def make_blob(ciphertext_token: bytes, salt: bytes) -> str:
    data = {
        "v": BLOB_VERSION,
        "alg": "fernet+hkdf",
        "salt": b64u_encode(salt),
        "ct": ciphertext_token.decode("utf-8"),
    }
    return json.dumps(data, separators=(",", ":"))

def parse_blob(blob_text: str):
    obj = json.loads(blob_text)
    if obj.get("v") != BLOB_VERSION or obj.get("alg") != "fernet+hkdf":
        raise ValueError("Unsupported blob format/version.")
    return b64u_decode(obj["salt"]), obj["ct"].encode("utf-8")

def encrypt_secret(secret: str, role: str):
    if not secret.strip():
        raise ValueError("Secret cannot be empty.")
    if not role.strip():
        raise ValueError("Role is required.")

    base_key = secrets.token_bytes(32)
    base_key_b64 = b64u_encode(base_key)
    salt = secrets.token_bytes(16)
    fernet_key = derive_fernet_key(base_key_b64, role, salt)
    cipher = Fernet(fernet_key)
    token = cipher.encrypt(secret.encode("utf-8"))

    blob = make_blob(token, salt)

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(blob)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    return blob, base_key_b64, img

def decrypt_secret(blob_text: str, base_key_b64: str, role: str) -> str:
    salt, token = parse_blob(blob_text)
    key = derive_fernet_key(base_key_b64, role, salt)
    cipher = Fernet(key)
    try:
        return cipher.decrypt(token).decode("utf-8")
    except InvalidToken:
        raise ValueError("Decryption failed. Check the base key and role.")

# ----------------- GUI App -----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("880x720")
        self.configure(bg="#f3e5f5")  # soft lilac

        self._apply_theme()

        header = tk.Label(
            self,
            text=APP_TITLE + " ✨",
            font=("Segoe UI", 20, "bold"),
            fg="#4a148c",
            bg="#f3e5f5",
            pady=10,
        )
        header.pack()

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=12)

        self.tab_enc = ttk.Frame(nb)
        self.tab_dec = ttk.Frame(nb)
        nb.add(self.tab_enc, text="💖 Encrypt (Create Blob)")
        nb.add(self.tab_dec, text="🔓 Decrypt (Use Blob)")

        self._build_encrypt_tab()
        self._build_decrypt_tab()

        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status, anchor="w").pack(fill="x", padx=12, pady=(0, 10))

        self._qr_photo = None

    def _apply_theme(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        bg = "#f3e5f5"           # soft lilac background
        lilac = "#ce93d8"        # tab/button bg
        dark_lilac = "#8e24aa"   # pressed
        princess_pink = "#f8bbd0" # hover/selected
        text = "#4a148c"

        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=text, font=("Segoe UI", 10))
        style.configure("TButton", background=lilac, foreground="black", padding=8, font=("Segoe UI", 10, "bold"))
        style.map("TButton",
                  background=[("active", princess_pink), ("pressed", dark_lilac)],
                  foreground=[("active", "black")])
        style.configure("TNotebook", background=lilac, tabmargins=[4, 6, 4, 0])
        style.configure("TNotebook.Tab", background=lilac, foreground="black", padding=[12, 8])
        style.map("TNotebook.Tab", background=[("selected", princess_pink)])

    def _build_encrypt_tab(self):
        f = self.tab_enc
        pad = {"padx": 10, "pady": 8}

        ttk.Label(f, text="Secret:").grid(row=0, column=0, sticky="w", **pad)
        self.enc_secret = tk.Text(f, height=7, wrap="word", bg="#fff0f6", fg="#4a148c")
        self.enc_secret.grid(row=1, column=0, columnspan=3, sticky="nsew", **pad)

        ttk.Label(f, text="Required Role:").grid(row=2, column=0, sticky="w", **pad)
        self.enc_role = ttk.Entry(f)
        self.enc_role.grid(row=2, column=1, sticky="ew", **pad)
        ttk.Button(f, text="✨ Create Blob", command=self._on_create_blob).grid(row=2, column=2, sticky="e", **pad)

        ttk.Label(f, text="Blob:").grid(row=3, column=0, sticky="w", **pad)
        self.blob_out = tk.Text(f, height=6, wrap="word", state="disabled", bg="#f3e5f5", fg="#4a148c")
        self.blob_out.grid(row=4, column=0, columnspan=3, sticky="nsew", **pad)

        ttk.Label(f, text="Base Key:").grid(row=5, column=0, sticky="w", **pad)
        self.key_out = tk.Text(f, height=2, wrap="none", state="disabled", bg="#f3e5f5", fg="#4a148c")
        self.key_out.grid(row=6, column=0, columnspan=3, sticky="nsew", **pad)

        btnrow = ttk.Frame(f)
        btnrow.grid(row=7, column=0, columnspan=3, sticky="ew", **pad)
        ttk.Button(btnrow, text="Copy Blob", command=lambda: self._copy_from(self.blob_out)).pack(side="left")
        ttk.Button(btnrow, text="Copy Base Key", command=lambda: self._copy_from(self.key_out)).pack(side="left")
        ttk.Button(btnrow, text="Save Blob to File", command=self._save_blob_file).pack(side="left")

        ttk.Label(f, text="QR Code:").grid(row=8, column=0, sticky="w", **pad)
        self.qr_label = ttk.Label(f)
        self.qr_label.grid(row=9, column=0, columnspan=3, sticky="n", **pad)

        f.grid_rowconfigure(1, weight=1)
        f.grid_rowconfigure(4, weight=1)
        f.grid_rowconfigure(6, weight=0)
        f.grid_rowconfigure(9, weight=1)
        f.grid_columnconfigure(2, weight=1)

    def _build_decrypt_tab(self):
        f = self.tab_dec
        pad = {"padx": 10, "pady": 8}

        ttk.Label(f, text="Blob:").grid(row=0, column=0, sticky="w", **pad)
        self.blob_in = tk.Text(f, height=8, wrap="word", bg="#fff0f6", fg="#4a148c")
        self.blob_in.grid(row=1, column=0, columnspan=3, sticky="nsew", **pad)
        ttk.Button(f, text="Load Blob From File", command=self._load_blob_file).grid(row=2, column=0, sticky="w", **pad)

        ttk.Label(f, text="Your Role").grid(row=3, column=0, sticky="w", **pad)
        self.dec_role = ttk.Entry(f)
        self.dec_role.grid(row=3, column=1, sticky="ew", **pad)

        ttk.Label(f, text="Base Key").grid(row=4, column=0, sticky="w", **pad)
        self.dec_key = ttk.Entry(f)
        self.dec_key.grid(row=4, column=1, sticky="ew", **pad)
        ttk.Button(f, text="💖 Decrypt", command=self._on_decrypt).grid(row=4, column=2, sticky="e", **pad)

        ttk.Label(f, text="Decrypted Secret").grid(row=5, column=0, sticky="w", **pad)
        self.dec_out = tk.Text(f, height=8, wrap="word", state="disabled", bg="#f3e5f5", fg="#4a148c")
        self.dec_out.grid(row=6, column=0, columnspan=3, sticky="nsew", **pad)

        ttk.Button(f, text="Copy Decrypted Secret", command=lambda: self._copy_from(self.dec_out)).grid(row=7, column=2, sticky="e", **pad)

        f.grid_rowconfigure(1, weight=1)
        f.grid_rowconfigure(6, weight=1)
        f.grid_columnconfigure(2, weight=1)

    # ----- Handlers -----
    def _on_create_blob(self):
        secret = self.enc_secret.get("1.0", "end").strip()
        role = self.enc_role.get().strip()
        try:
            blob, base_key_b64, qr_img = encrypt_secret(secret, role)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Failed to create blob.")
            return
        self._write_text(self.blob_out, blob)
        self._write_text(self.key_out, base_key_b64)
        self.status.set("Blob created — share with magic ✨")
        qr_img = qr_img.resize((280, 280))
        self._qr_photo = ImageTk.PhotoImage(qr_img)
        self.qr_label.configure(image=self._qr_photo)

    def _save_blob_file(self):
        blob = self.blob_out.get("1.0", "end").strip()
        if not blob:
            messagebox.showinfo("Nothing to save", "Create a blob first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".spaste", filetypes=[("Secure Paste Blob", "*.spaste")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(blob)
            self.status.set(f"Saved blob to {os.path.basename(path)}")

    def _load_blob_file(self):
        path = filedialog.askopenfilename(filetypes=[("Secure Paste Blob", "*.spaste")])
        if path:
            with open(path, "r", encoding="utf-8") as f:
                blob = f.read()
            self.blob_in.delete("1.0", "end")
            self.blob_in.insert("1.0", blob)
            self.status.set(f"Loaded blob from {os.path.basename(path)}")

    def _on_decrypt(self):
        blob = self.blob_in.get("1.0", "end").strip()
        role = self.dec_role.get().strip()
        base_key_b64 = self.dec_key.get().strip()
        try:
            pt = decrypt_secret(blob, base_key_b64, role)
            self._write_text(self.dec_out, pt)
            self.status.set("Decrypted successfully 💎")
        except Exception as e:
            messagebox.showerror("Decryption failed", str(e))
            self.status.set("Decryption failed.")

    def _write_text(self, widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    def _copy_from(self, widget):
        text = widget.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("Nothing to copy", "Nothing to copy.")
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status.set("Copied to clipboard.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
