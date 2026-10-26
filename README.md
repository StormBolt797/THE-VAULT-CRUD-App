# The Vault

A web app built with Python and Flask for storing files and notes privately in the cloud. It encrypts uploaded files using AES-256 before saving them to a PostgreSQL database, lets you generate 24 hour shareable download links, has a trash bin with restore support, and includes a slide out quick notes panel.

Live Demo: https://the-vault-wzzb.onrender.com

---

## Features

### AES-256 File Encryption
Files are encrypted with `cryptography.fernet` (AES-256) before getting saved to the database. When a user requests a download, the app decrypts the file in memory using `io.BytesIO` and streams it directly to the browser. Raw files are never written to disk in plaintext.

### 24-Hour Shareable Links
Users can generate temporary download links for any file. These links use unique tokens (`/s/<token>`) and automatically expire after 24 hours so guests can download a file without creating an account.

### Trash Bin and File Recovery
Deleting a file marks it as soft deleted instead of removing it immediately. You can view all deleted files in the Trash page, restore them back to your vaultbox, or permanently purge them.

### Quick Notes Panel
A WhatsApp style side drawer on the right side of the screen. You can type quick notes, edit them in place, delete them, or download all notes as a text file.

### Search and Filter
Filter your files instantly by name or by type (Images, Docs) using real time search on the client side.

### Authentication
User accounts use `Flask-Login` for sessions and `werkzeug.security` for password hashing with salted `scrypt`.

### Cloud and Local Database
Uses PostgreSQL when hosted online (Render) via `DATABASE_URL`, and automatically falls back to local SQLite (`database.db`) when running offline on your computer.

---

## Tech Stack

* Python 3
* Flask
* PostgreSQL (production) and SQLite (local)
* Flask-SQLAlchemy (ORM)
* Flask-Login
* Werkzeug (password hashing)
* Cryptography (Fernet AES-256)
* Gunicorn
* HTML, CSS, Bootstrap 4, JavaScript

---

## How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/StormBolt797/THE-VAULT-CRUD-App.git
   cd THE-VAULT-CRUD-App
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   *(On Windows use `venv\Scripts\activate`)*

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python main.py
   ```

5. Open `http://127.0.0.1:5000/` in your browser. The SQLite database will be created automatically.

---

## Contact

Developer: Siddharth R  
Email: siddharth.official77@gmail.com  
Phone: +91 9384849418
