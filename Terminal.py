import sys
from PyQt6.QtWidgets import QApplication, QMainWindow,QListWidgetItem, QVBoxLayout, QTextEdit, QLineEdit, QWidget, QMessageBox, QPushButton, QHBoxLayout, QInputDialog
from PyQt6.QtGui import QAction
import os
import subprocess
import time
from bs4 import BeautifulSoup
import speech_recognition as sr
from PyQt6.QtWidgets import QCompleter
from PyQt6.QtCore import QStringListModel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon




class TerminalWindow(QMainWindow):
    def __init__(self, command_list=None):
        super().__init__()
        self.setWindowTitle("Fire Terminal")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)
        terminal_layout = QVBoxLayout()
        button_layout = QVBoxLayout()

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        terminal_layout.addWidget(self.output_text)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Kullanılabilir komutlar için -help yazın.")
        terminal_layout.addWidget(self.input_line)
        self.input_line.returnPressed.connect(self.run_command)

        self.memory = {}

        main_layout.addLayout(terminal_layout)
        main_layout.addLayout(button_layout)

        self.command_history = []

        # Menü Çubuğu
        menubar = self.menuBar()

        # Tema Menüsü
        theme_menu = menubar.addMenu("Tema")
        light_theme_action = QAction("Açık Tema", self)
        light_theme_action.triggered.connect(lambda: self.change_theme('light'))
        dark_theme_action = QAction("Koyu Tema", self)
        dark_theme_action.triggered.connect(lambda: self.change_theme('dark'))
        grey_theme_action = QAction("Gri Tema", self)
        grey_theme_action.triggered.connect(lambda: self.change_theme('grey'))
        theme_menu.addAction(light_theme_action)
        theme_menu.addAction(dark_theme_action)
        theme_menu.addAction(grey_theme_action)

        # Diğer menüler
        # Komut Geçmişi Menüsü
        history_menu = menubar.addMenu("Komut Geçmişi")
        history_action = QAction("Göster", self)
        history_action.triggered.connect(self.show_command_history)
        history_menu.addAction(history_action)

        # Ayarlar Menüsü
        settings_menu = menubar.addMenu("Hesabım")
        settings_action = QAction("Hesabım", self)
        settings_action.triggered.connect(self.settings_action)
        settings_menu.addAction(settings_action)

        # Özellikler Menüsü
        features_menu = menubar.addMenu("Özellikler")
        features_action = QAction("Özellikler", self)
        features_action.triggered.connect(self.features_action)
        features_menu.addAction(features_action)

        # Hesabım Menüsü
        account_menu = menubar.addMenu("Ayarlar")
        account_action = QAction("Ayarlar", self)
        account_action.triggered.connect(self.account_action)
        account_menu.addAction(account_action)

        # Butonlar
        commands = [
            ("-help", "Help", "help_icon.png"), 
            ("-clear", "Clear", "clear_icon.png"), 
            ("-ls", "List", "list_icon.png"), 
            ("-pwd", "Pwd", "pwd_icon.png"), 
            ("-voice", "Voice", "voice_icon.png")
        ]

        for command, text, icon_path in commands:
            button = QPushButton(text)  # Buton metnini ayarla
            button.setIcon(QIcon(icon_path))  # İkon ekleme
            button.setToolTip(command)  # Tooltip olarak orijinal komut
            button.clicked.connect(lambda checked, cmd=command: self.run_command_from_button(cmd))
            button.setStyleSheet("""
                QPushButton {
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
            button_layout.addWidget(button)

        self.command_list = ["-help", "-clear", "-ls", "-pwd", "-cat", "-mkdir", "-rmdir", "-cp", "-mv", "-run", "-open", "-sunum", "-youtube", "-voice", "-not", "-locals", "-rm", "-touch", "-rename", "-search", "-python", "-exit", "-openurl"]
        completer = QCompleter(self.command_list, self)
        self.input_line.setCompleter(completer)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCaseSensitivity(Qt.CaseSensitivity(0)) 
 
  

        
    

    def change_theme(self, theme):
        if theme == 'dark':
            self.setStyleSheet("background-color: #000000; color: #ffffff;")  # Ana pencere siyah, yazı beyaz
            self.output_text.setStyleSheet("background-color: #000000; color: #ffffff;")  # Çıktı alanı siyah, yazı beyaz
            self.input_line.setStyleSheet("background-color: #000000; color: #ffffff;")  # Girdi alanı siyah, yazı beyaz
        elif theme == 'grey':
            self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")  # Ana pencere koyu gri, yazı beyaz
            self.output_text.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")  # Çıktı alanı koyu gri, yazı beyaz
            self.input_line.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")  # Girdi alanı koyu gri, yazı beyaz
        else:  # Light theme
            self.setStyleSheet("background-color: #ffffff; color: #000000;")  # Ana pencere beyaz, yazı siyah
            self.output_text.setStyleSheet("background-color: #ffffff; color: #000000;")  # Çıktı alanı beyaz, yazı siyah
            self.input_line.setStyleSheet("background-color: #ffffff; color: #000000;")  # Girdi alanı beyaz, yazı siyah
        self.current_theme = theme



    def run_voice_command(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

    def run_command_from_button(self, command):
        self.input_line.setText(command)
        self.run_command()

    def run_command(self):
        commands = self.input_line.text().split(";")
        self.input_line.clear()
        

        for command in commands:
            command = command.strip()
            self.command_history.append(command)
            self.output_text.append(f">>> {command}")

            if "=" in command:
                parts = command.split("=")
                var_name = parts[0].strip()
                expression = "=".join(parts[1:]).strip()

                try:
                    result = eval(expression, {}, self.memory)
                    self.memory[var_name] = result
                    self.output_text.append(f"{var_name} = {result}")
                except Exception as e:
                    self.output_text.append(f"Error: {e}")
            elif command.startswith("-search "):
                self.search_web(command[len("-search "):])
            else:
                if command.startswith("-"):
                    self.handle_builtin_commands(command)
                else:
                    try:
                        result = eval(command, {}, self.memory)
                        self.output_text.append(str(result))
                    except Exception as e:
                        self.output_text.append(f"Error: {e}")

    def handle_builtin_commands(self, command):
        if command == "-exit":
            self.close()
        elif command == "-help":
            self.output_text.append("""Available commands:
        -help: Show this help message
        -clear: Clear the terminal
        -ls: List files in the current directory
        -pwd: Print working directory
        -cat <file>: Display file content
        -mkdir <dir>: Create a directory
        -rmdir <dir>: Remove a directory
        -cp <file1> <file2>: Copy file1 to file2
        -mv <file1> <file2>: Move file1 to file2
        -run <script>: Run a Python script
        -open <file>: Open a file
        -sunum: Open Canva for presentations
        -youtube: Open YouTube Music
        -voice: Execute a voice command
        -not: Open Notes application
        -locals <keyword>: Search for a keyword in local .txt files
        -rm <file>: Remove a file
        -touch <file>: Create an empty file
        -rename <old> <new>: Rename a file or directory
        -search <query>: Search the web
        -python: Enter Python interactive mode
        -exit: Exit the terminal application
        -openurl <url>: Open a URL in the default web browser
        """)


        
        elif command == "-clear":
            self.output_text.clear()
            self.memory.clear()
        elif command == "-ls":
            file_list = os.listdir()
            self.output_text.append("\n".join(file_list))
        elif command == "-pwd":
            current_dir = os.getcwd()
            self.output_text.append(current_dir)
        elif command.startswith("-cat"):
            file_name = command.split(" ")[1]
            if os.path.exists(file_name):
                with open(file_name, "r") as file:
                    content = file.read()
                    self.output_text.append(content)
            else:
                self.output_text.append(f"File not found: {file_name}")
       
        elif command.startswith("-mkdir"):
            dir_name = command.split(" ")[1]
            os.mkdir(dir_name)
            self.output_text.append(f"Directory created: {dir_name}")
        elif command.startswith("-rmdir"):
            dir_name = command.split(" ")[1]
            os.rmdir(dir_name)
            self.output_text.append(f"Directory removed: {dir_name}")
        elif command.startswith("-cp"):
            file1, file2 = command.split(" ")[1:]
            os.system(f"cp {file1} {file2}")
            self.output_text.append(f"{file1} copied to {file2}")
        elif command.startswith("-mv"):
            file1, file2 = command.split(" ")[1:]
            os.system(f"mv {file1} {file2}")
            self.output_text.append(f"{file1} moved to {file2}")
        elif command.startswith("-run "):
            script_path = command[len("-run "):].strip()
            self.run_python_script(script_path)
        elif command.startswith("-rm"):
            file_name = command.split(" ")[1]
            os.remove(file_name)
            self.output_text.append(f"File removed: {file_name}")
        elif command.startswith("-touch"):
            file_name = command.split(" ")[1]
            open(file_name, 'a').close()
            self.output_text.append(f"File created: {file_name}")
        elif command.startswith("-rename"):
            old_name, new_name = command.split(" ")[1:]
            os.rename(old_name, new_name)
            self.output_text.append(f"{old_name} renamed to {new_name}")

        elif command.startswith("-open"):
            file_name = command.split(" ")[1]
            os.system(f"open {file_name}")
            self.output_text.append(f"{file_name} opened")
        elif command == "-python":
            self.run_python_interactive_mode()
        elif command == "-sunum":
            os.system("open https://www.canva.com")
            self.output_text.append("Sunum başlatıldı.")
        elif command == "-youtube":
            os.system("open https://music.youtube.com")
            self.output_text.append("YouTube Music açıldı.")
        elif command == "-voice":
            self.run_voice_command()
        
        elif command == "-not":
            os.system("open -a Notes")
            self.output_text.append("Notes açıldı.")
        elif command.startswith("-locals"):
            keyword, ok_pressed = QInputDialog.getText(self, "Local File Search", "Enter keyword:")
            if ok_pressed:
                self.search_local_files(keyword.strip())
            else:
                self.output_text.append("No keyword entered.")
        elif command.startswith("-rm "):
            file_name = command.split(" ")[1]
            if os.path.exists(file_name):
                os.remove(file_name)
                self.output_text.append(f"File removed: {file_name}")
            else:
                self.output_text.append(f"File not found: {file_name}")
        elif command.startswith("-openurl "):
            url = command.split(" ")[1]
            self.open_url(url)

        elif command.startswith("-touch "):
            file_name = command.split(" ")[1]
            open(file_name, 'a').close()
            self.output_text.append(f"File created: {file_name}")
        elif command.startswith("-rename "):
            old_name, new_name = command.split(" ")[1:]
            if os.path.exists(old_name):
                os.rename(old_name, new_name)
                self.output_text.append(f"{old_name} renamed to {new_name}")
            else:
                self.output_text.append(f"File or directory not found: {old_name}")
    def search_local_files(self, keyword):
    # Anahtar kelimeyi kullanarak yerel dosyalarda arama yap
        matches = []
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        if keyword in f.read():
                            matches.append(filepath)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

        # Eşleşen dosyaları çıktıya
        if matches:
            self.output_text.append("Matching files found:")
            for match in matches:
                self.output_text.append(match)
        else:
            self.output_text.append("No matching files found.")
    
    def get_user_input(self, prompt):
        self.input_line.setPlaceholderText(prompt)
        self.input_line.setFocus()  # Kullanıcının hemen giriş yapabilmesi için odaklan
        self.input_line.returnPressed.connect(self.handle_user_input)  # Girişe basıldığında kullanıcı girişini işle
        self.user_input = None  # Kullanıcı girişini tutmak için bir değişken tanımla
    # Kullanıcının giriş yapmasını bekleyin
        while self.user_input is None:
            QApplication.processEvents()  # Arayüz etkinliklerini işle
    # Giriş yapıldıktan sonra bağlantıyı kaldır
        self.input_line.returnPressed.disconnect(self.handle_user_input)
        return self.user_input

    def handle_user_input(self):
        self.user_input = self.input_line.text()
    
    def run_python_script(self, script_path):
        try:
            with open(script_path, "r") as script_file:
                script_code = script_file.read()
                exec_result = exec(script_code, {}, self.memory)
                if exec_result is not None:
                    self.output_text.append(str(exec_result))
                else:
                    self.output_text.append("Python script executed successfully.")
        except Exception as e:
            self.output_text.append(f"Error executing Python script: {e}")

    def run_python_interactive_mode(self):
        self.output_text.append("Entering Python interactive mode. Type '-exit' to exit.")
        code_lines = []

        while True:
            prompt = ">>> " if not code_lines else "... "
            user_input = self.get_user_input(prompt)

            if user_input.strip() == "-ex":
                self.output_text.append("Exited Python interactive mode.")
                return "Exited Python interactive mode."  # Fonksiyon çıktığında dönüş yap
            else:
                code_lines.append(user_input)

                try:
                # Tek bir string olarak kodu birleştir
                    code_to_run = "\n".join(code_lines)
                
                # exec komutunun çıktısını almak için
                    exec_locals = {}
                    exec(code_to_run, {}, exec_locals)
                
                # Çıktıları terminal penceresine ekle
                    if exec_locals:
                        for var, value in exec_locals.items():
                            self.output_text.append(f"{var} = {value}")

                except Exception as e:
                    self.output_text.append(f"Error: {e}")
                    code_lines.clear()

    def on_return_pressed(self):
        command = self.input_line.text()
        print(f"Running command: {command}")
    def run_voice_command(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        try:
            with mic as source:
                self.output_text.append("Listening for command...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                self.output_text.append(f"Voice command: {command}")
                self.input_line.setText("-" + command)
                self.run_command()
        except sr.UnknownValueError:
            self.output_text.append("Sesli komut anlaşılmadı.")
        except sr.RequestError as e:
            self.output_text.append(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            self.output_text.append(f"Error: {e}")

    def open_url(self, url):
        try:
            os.system(f"open {url}")
            self.output_text.append(f"Opened URL: {url}")
        except Exception as e:
            self.output_text.append(f"Error opening URL: {e}")
 
    def search_web(self, query):
        search_query = query.replace(" ", "+")
        search_url = f"https://www.google.com/search?q={search_query}"

        # Safari'de arama yap
        subprocess.run(["open", "-a", "Safari", search_url])

        # Bir süre bekleyip ardından sayfanın içeriğini çekmek için bu örnekte BeautifulSoup kullanılıyor
        time.sleep(5)  # Bu süreyi gerektiği gibi ayarlayın

        # Selenium veya benzeri bir kütüphane kullanmadan bu işlemi yapmak zordur
        # Aşağıdaki kod, sadece örnek amaçlıdır ve gerçek bir çözüm değildir
        try:
            # Geçici olarak sonuçları bir HTML dosyasına kaydedin
            with open("results.html", "w") as f:
                subprocess.run(["curl", search_url], stdout=f)

            # HTML dosyasını okuyun
            with open("results.html", "r") as f:
                soup = BeautifulSoup(f, "html.parser")

            # İlk sonucun URL'sini bulun
            first_result = soup.find('a')
            if first_result and 'href' in first_result.attrs:
                first_result_url = first_result['href']
                self.output_text.append(f"First result URL: {first_result_url}")
            else:
                self.output_text.append("No results found.")
        except Exception as e:
            self.output_text.append(f"Error during web search: {e}")

    def show_command_history(self):
        # Komut geçmişini göstermek için bir iletişim kutusu oluşturun
        history_text = "\n".join(self.command_history)
        QMessageBox.information(self, "Command History", history_text)

    def show_suggestions(self):
        # Giriş kutusundaki metni al
        text = self.input_line.text().strip()

        # Önerileri temizle
        self.suggestion_list.clear()

        if text and text.startswith("-"):
            # Giriş metni bir komutla başlıyorsa, uygun önerileri göster
            suggestions = [cmd for cmd in self.command_list if cmd.startswith(text)]
            for suggestion in suggestions:
                item = QListWidgetItem(suggestion)
                self.suggestion_list.addItem(item)

            # Önerileri göster
            if suggestions:
                self.suggestion_list.show()
            else:
                self.suggestion_list.hide()
        else:
            # Giriş metni bir komutla başlamıyorsa, önerileri gizle
            self.suggestion_list.hide()


    def settings_action(self):
        QMessageBox.information(self, "Hesabım", "Hesabım penceresi burada açılacak.")
        
    def features_action(self):
        QMessageBox.information(self, "Özellikler", "Özellikler penceresi burada açılacak.")

    def account_action(self):
        QMessageBox.information(self, "Ayarlar", "Ayarlar penceresi burada açılacak.")
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    command_list = ["-help", "-ls", "-pwd", "-exit"]
    window = TerminalWindow(command_list)
    window.show()
    sys.exit(app.exec())