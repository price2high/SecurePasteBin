# Usage

## Encrypt (Create Blob)
1) Open the app → **Encrypt** tab.
2) Paste your secret (password/code/note).
3) Set **Required Role** (e.g., `admin`, `dev`). The role becomes part of key derivation.
4) Click **Create Blob**.
5) Share:
   - **Blob** (copy as text, save to `.spaste`, or share via QR)
   - **Base Key** (send via a different channel: phone call/SMS)

## Decrypt (Use Blob)
1) Open the app → **Decrypt** tab.
2) Paste the blob (or **Load Blob From File**).
3) Enter **Your Role** and the **Base Key** shared by the sender.
4) Click **Decrypt** to reveal the secret.

## Tips
- “Burn after read” → delete the `.spaste` or message after delivery.
- Keep base keys out of chat logs; prefer a phone call or separate secure channel.
- Roles are free-form strings; agree on them beforehand (e.g., `ops`, `finance`, `oncall`). Consistency matters.
