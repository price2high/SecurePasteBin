# Threat Model

## Assets
- Secret plaintext.
- Base key (highest sensitivity).
- Role string (must match; part of KDF).

## Adversary
- Can intercept or read the blob.
- Cannot decrypt without base key **and** correct role.

## Risks & Mitigations
- **Key leakage via chat logs** → send keys by voice or separate channel.
- **Clipboard snooping** → clear clipboard after use; avoid shared machines.
- **Phishing of role names** → pick non-obvious roles or add a passphrase prefix.
- **Malware on endpoints** → this app cannot protect an already-compromised device.
- **User error** (wrong role/key) → decryption fails safely; no partial plaintext.

## Out of Scope
- Centralized key management, rotation, and audit trails.
- Multi-party approvals or quorum encryption.
