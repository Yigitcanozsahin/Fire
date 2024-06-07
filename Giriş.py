import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtCore import Qt, pyqtSignal  # Import QtCore along with other modules
import hashlib
import re
import subprocess
# Veritabanı ve tablo oluşturma
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Yeni kullanıcı ekleme
def add_user(username, email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Parola şartlarını kontrol et
    if not is_password_strong(password):
        QMessageBox.warning(None, "Warning", "Password is not strong enough.")
        return

    # Parolayı hash'le
    password_hash = hash_password(password)
    print(f"Hashlenmiş Parola: {password_hash}")  # Debug için eklendi

    try:
        c.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))
        conn.commit()
        QMessageBox.information(None, "Success", "User registration successful!")
        print(f"Kullanıcı Eklendi: {username}, {email}")  # Debug için eklendi
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed: users.username' in str(e):
            QMessageBox.warning(None, "Warning", f"User {username} already exists.")
        elif 'UNIQUE constraint failed: users.email' in str(e):
            QMessageBox.warning(None, "Warning", f"Email {email} already exists.")
        else:
            QMessageBox.warning(None, "Warning", f"An error occurred: {str(e)}")
    conn.close()


# Kullanıcı doğrulama
def validate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user is None:
        return False

    # Parolayı hash'le ve karşılaştır
    password_hash = hash_password(password)
    return user[3] == password_hash

# Parolanın gücünü kontrol et
def is_password_strong(password):
    # Örnek parola şartları: En az 8 karakter, en az bir büyük harf, bir küçük harf ve bir rakam içermelidir.
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)

# Parolayı hash'le
def hash_password(password):
    # Parolayı SHA-256 algoritmasıyla hash'le
    return hashlib.sha256(password.encode()).hexdigest()

# E-posta adresinin doğruluğunu kontrol et
def is_valid_email(email):
    # Basit bir e-posta doğrulama deseni kullanarak e-posta adresinin geçerliliğini kontrol edin
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 300, 250)
        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout(self)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.password_confirm_input = QLineEdit(self)
        self.password_confirm_input.setPlaceholderText("Confirm Password")
        self.password_confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_confirm_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.setObjectName("myButton")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        password_confirm = self.password_confirm_input.text()

        if not (username and email and password and password_confirm):
            QMessageBox.warning(None, "Warning", "Please fill in all fields.")
            return

        if not is_valid_email(email):
            QMessageBox.warning(None, "Warning", "Please enter a valid email address.")
            return

        if password != password_confirm:
            QMessageBox.warning(None, "Warning", "Passwords do not match.")
            return

        add_user(username, email, password)

        # Kayıt işlemi başarılı olduğunda pencereyi kapat
        self.close()

class LoginWindow(QWidget):
    # Define login_successful signal here
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)
        self.create_widgets()


    def create_widgets(self):
        layout = QVBoxLayout(self)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.setObjectName("myButton")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # Kullanıcıyı doğrula
        if validate_user(username, password):
            self.login_successful.emit()
            self.close()

            # Giriş başarılı olduğunda scripti çalıştır
            subprocess.run(["python3", "/Users/yigitcanozsahin/Desktop/Fire/Terminal.py"])
        else:
            QMessageBox.warning(self, "Warning", "Invalid username or password.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FİRE")
        self.setGeometry(100, 100, 300, 150)
        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout()

        self.login_button = QPushButton("Login", self)
        self.login_button.setObjectName("myButton")
        self.login_button.clicked.connect(self.show_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register", self)
        self.register_button.setObjectName("myButton")
        self.register_button.clicked.connect(self.show_register)
        layout.addWidget(self.register_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_login(self):
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.on_login_successful)
        self.login_window.show()

    def show_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def on_login_successful(self):
        QMessageBox.information(self, "Success", "Login successful!")


def main():
    create_db()

    app = QApplication(sys.argv)
    app.setStyleSheet("""
    #myButton {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 10px;
    }
""")

    screen_resolution = app.primaryScreen()
    # Ekranın yüzde 80'ini kaplayacak şekilde boyutlandırın
    window_size = screen_resolution.size()
    window_width = window_size.width() * 0.4
    window_height = window_size.height() * 0.8

    window = MainWindow()
    window.resize(int(window_width), int(window_height))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
