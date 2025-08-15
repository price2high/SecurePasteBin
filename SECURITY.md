# Security Model

**Goal:** End-to-end encryption without a server. The app never sends data over the network.

## Design
- A random **base key** (32 bytes, urlsafe base64) is generated per secret.
- A random **salt** (16 bytes) is embedded in the blob.
- A Fernet key is **derived with HKDF-SHA256** over `(base key, role, salt)`.
- The secret is encrypted with **Fernet** (spec: AES-128-CBC + HMAC-SHA256; 32-byte key split for encrypt/auth).

```
derived_key = HKDF(salt=salt, info="secure-paste-p2p|role:<role>|v:1")(base_key)
fernet_key  = base64.urlsafe_b64encode(derived_key)  # 32 bytes → Fernet format
ciphertext  = Fernet(fernet_key).encrypt(plaintext)
blob = { v:1, alg:"fernet+hkdf", salt:b64u(salt), ct:ciphertext_b64 }
```

## Properties
- **E2E**: Only holders of the **base key** and exact **role** can derive the Fernet key.
- **Forward secrecy (per secret)**: Each secret has a new random base key and salt.
- **Salt in blob**: Safe to store; needed for KDF reproducibility.

## What this does **not** solve
- Endpoint compromise (malware/clipboard stealers).
- Social engineering (wrong “role” or base key sent to an attacker).
- Revocation at scale (no central server; sender must manually delete blobs).

## Recommendations
- Share base keys via **separate channel** (voice/SMS).
- Prefer **short-lived** sharing: delete blobs after use.
- Consider password managers for long-term storage and audit requirements.
