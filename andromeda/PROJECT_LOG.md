# Andromeda Vault: Development Log (Trials & Errors)

This file records the development progress, bugs encountered, and solutions applied.

## Phase 1: Basic CRUD (Create, Read, Update, Delete)
**Goal:** Add Edit and Delete capabilities to password entries.

* **Trial:** Added Edit/Delete buttons to the table.
* **Error:** The table layout "broke" when clicking to reveal a password.
    * *Cause:* We were using `display: none` on the entire cell (`<td>`), causing subsequent cells to shift to the left.
* **Fix:** Changed the logic in `index.html`. The cell remains visible, and we only toggle the visibility (`display`) between two `<span>` elements (Mask vs Secret) inside the cell.

## Phase 2: Login System & UI
**Goal:** Protect the page with a Login system and Sci-Fi Design.

* **Trial:** Applied Glassmorphism UI and removed the Register route for security.
* **Error:** `werkzeug.routing.exceptions.BuildError: Could not build url for endpoint 'register'.`
    * *Cause:* We deleted the route (`@app.route('/register')`) from `app.py`, but forgot to remove the `<a href...>` link from `login.html`.
* **Fix:** Removed the "Create Account" link from the HTML.

## Phase 3: Security Hardening (2FA)
**Goal:** Add Google Authenticator (TOTP) and QR Code.

* **Trial 1:** Installed `pyotp` and `qrcode`, updated the database.
* **Error:** `ModuleNotFoundError: No module named 'PIL'` during QR generation.
    * *Cause:* The `qrcode` library requires `pillow` to draw the image, but it was missing.
* **Fix:** `pip3 install pillow`.

* **Trial 2:** Attempted to view QR Code after installing Pillow.
* **Error:** The system went directly to the "Verify Code" input without showing the QR.
    * *Cause:* During Trial 1 (before the crash), the system managed to save a secret key to the database. When logging in again, it assumed setup was already complete.
* **Fix:** Created `reset_2fa.py` script to run `UPDATE users SET totp_secret = NULL` to restart the setup process.

## Phase 4: HTTPS (SSL)
**Goal:** Connection encryption.

* **Action:** Created Self-Signed Certificates using OpenSSL.
* **Result:** Browser displays "Not Secure" warning.
    * *Explanation:* Expected behavior for self-signed certificates. We click "Proceed Anyway". Encryption works normally.
