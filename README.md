# The Vault - CRUD Application

A local web application built with Python and Flask that serves as a personal vault for storing, managing, and downloading files and notes securely using SQLite.

---

## Features

- **User Authentication & Authorization**:
  - Secure user registration and login system.
  - Passwords hashed using `werkzeug.security` (`generate_password_hash` / `check_password_hash`).
  - Session and route protection managed via `flask_login`.

- **File Management (C.R.U.D)**:
  - **Upload**: Store images, PDFs, and documents directly in the local SQLite database as binary data (`LargeBinary` / BLOB).
  - **Download / Read**: Stream stored files back to the browser on demand via `BytesIO`.
  - **Delete**: Permanently remove stored files from records.

- **Personal Notes**:
  - Inbuilt notepad feature allowing users to create and store timestamped personal notes associated with their account.

---

## Tech Stack

- **Backend**: Python, Flask, Jinja2
- **Database & ORM**: SQLite, Flask-SQLAlchemy
- **Authentication**: Flask-Login, Werkzeug Security
- **Frontend**: HTML5, CSS3, Bootstrap 4

---

## Project Structure

```text
THE-VAULT-CRUD-App/
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies
├── README.md                # Project documentation
└── website/                 # Application package
    ├── __init__.py          # App initialization & database configuration
    ├── auth.py              # Authentication blueprint (login, signup, logout)
    ├── models.py            # SQLAlchemy database models (User, Userfiles)
    ├── views.py             # Core routes (file upload, download, delete, notes)
    └── templates/           # Jinja2 HTML templates
        ├── index.html       # Base layout & navigation bar
        ├── home.html        # Main dashboard
        ├── login.html       # User login page
        ├── signup.html      # Account registration page
        ├── fileupload.html  # File upload form
        ├── download.html    # File download selector
        ├── delete.html      # File deletion selector
        └── notes.html       # Notes creator
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher installed on your system.

### Installation & Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/StormBolt797/THE-VAULT-CRUD-App.git
   cd THE-VAULT-CRUD-App
   ```

2. **Set up a virtual environment** *(optional but recommended)*:
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt flask_sqlalchemy flask_login
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Open in browser**:
   Navigate to `http://127.0.0.1:5000/`.
   The SQLite database (`database.db`) is automatically initialized upon startup.

---

## Contact

For any queries, reach out at `me25b122@smail.iitm.ac.in`.
