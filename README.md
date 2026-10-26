# The Vault - Cloud-Native Encrypted Vaultbox

A full-stack secure cloud storage and document vault platform built with Python, Flask, and PostgreSQL (with local SQLite fallback). Features client-isolated AES-256 binary encryption, time-expiring shareable download tokens, real-time file filtering, and soft-delete trash recovery.

---

## Key Features

- **End-to-End At-Rest File Encryption (AES-256)**:
  - All binary payloads are dynamically encrypted using `cryptography.fernet` before persisting to PostgreSQL byte columns.
  - Files are decrypted on the fly in volatile server memory (`io.BytesIO`) upon authorized retrieval.

- **Expiring & Tokenized Shareable Links**:
  - Authenticated users can generate cryptographically random tokenized URLs (`/s/<token>`) to delegate read-only downloads to external guests without exposing accounts.

- **Lifecycle & Soft-Delete Trash Bin**:
  - Files moved to a dedicated Trash Bin instead of immediate destructive deletion, supporting one-click restoration or irreversible permanent purging.

- **Real-Time Client-Side Search & Categorization**:
  - Instant name-based search and categorical filtering (`All`, `Images`, `Documents`, `Notes`) with human-readable file sizes (`KB`, `MB`).

- **Secure Authentication & Identity**:
  - User registration and login protected by `werkzeug.security` salted password hashing (`scrypt`) and session control via `flask_login`.

- **Hybrid Database Architecture**:
  - Automatically targets cloud PostgreSQL when `DATABASE_URL` is set, seamlessly falling back to local SQLite (`database.db`) for offline development.

---

## Tech Stack

- **Backend**: Python 3, Flask, Jinja2, Gunicorn
- **Database & ORM**: PostgreSQL (Cloud), SQLite (Local Fallback), Flask-SQLAlchemy
- **Security & Crypto**: Cryptography (Fernet / AES-256), Werkzeug Security (`scrypt`), Secrets/UUID
- **Frontend**: HTML5, CSS3, Bootstrap 4, FontAwesome, JavaScript

---

## Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/StormBolt797/THE-VAULT-CRUD-App.git
   cd THE-VAULT-CRUD-App
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run locally**:
   ```bash
   python main.py
   ```
   Open `http://127.0.0.1:5000/`. Local SQLite database is created automatically.

---

## Contact

Developer: Siddharth R  
Email: `siddharth.official77@gmail.com`  
Phone: `+91 9384849418`
