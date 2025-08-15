# FAQ

**Is this safer than sending passwords in chat?**  
Yes — blobs are ciphertext only. The base key is required to decrypt and should be sent via a *different* channel.

**What if someone steals the blob?**  
They still need the base key *and* the exact role string. Without those, decryption fails.

**Can I set a password instead of a role?**  
Yes — a role is essentially a label; you can use a passphrase or combine both (e.g., `ops:summer-rose-2025`).

**Does the app phone home or use a server?**  
No. Everything runs locally; sharing is via your existing channels (email/chat/QR).

**Can I add “burn-after-read” automatically?**  
This P2P variant is manual — delete the blob after first delivery. A centralized store variant can automate that.
