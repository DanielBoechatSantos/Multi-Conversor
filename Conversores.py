import sys
import os
import subprocess
import urllib.request
import zipfile
import shutil
import ctypes
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QComboBox, QFileDialog, QListWidget, QMessageBox, QProgressBar, QFrame, QGridLayout,
    QInputDialog 
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize, QTimer, QDateTime, QLocale
from PyQt5.QtGui import QIcon, QFont, QColor
from pydub import AudioSegment
from PIL import Image

# ----------- FUNÇÃO ESSENCIAL PARA EXE (PyInstaller) -----------
def resource_path(relative_path):
    """ Obtém o caminho absoluto do recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ----------- CONFIGURAÇÕES DO FFMPEG -----------
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_DIR = r"C:\ffmpeg"
FFMPEG_BIN = os.path.join(FFMPEG_DIR, "bin")

if os.path.exists(FFMPEG_BIN):
    os.environ["PATH"] += os.pathsep + FFMPEG_BIN

# ----------- ESTILO MODERNO (CSS) -----------
STYLE = """
    /* Fundo Geral */
    QWidget { 
        background-color: #121212; 
        color: #E0E0E0; 
        font-family: 'Segoe UI', sans-serif; 
        font-size: 10pt; 
    }

    /* Botões Principais (Tiles) */
    QPushButton.tile {
        background-color: #1E1E1E;
        border: 2px solid #333;
        border-radius: 15px;
        color: #FFF;
        font-size: 11pt;
        font-weight: bold;
        padding: 20px;
        text-align: center;
    }
    QPushButton.tile:hover {
        background-color: #2D2D2D;
        border-color: #3B82F6;
        color: #3B82F6;
    }
    QPushButton.tile:pressed {
        background-color: #0F172A;
    }

    /* Botões de Ação */
    QPushButton.action {
        background-color: #3B82F6;
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-weight: bold;
        color: white;
    }
    QPushButton.action:hover { background-color: #2563EB; }
    QPushButton.action:disabled { background-color: #475569; color: #94A3B8; }

    /* Inputs e Listas */
    QComboBox, QListWidget {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 8px;
        color: #FFF;
        font-size: 11pt;
    }
    QListWidget::item { padding: 8px; }
    QListWidget::item:selected { background-color: #3B82F6; }

    /* Barra de Progresso */
    QProgressBar {
        border: 2px solid #333;
        border-radius: 8px;
        text-align: center;
        background-color: #1E1E1E;
        color: white;
        font-weight: bold;
    }
    QProgressBar::chunk {
        background-color: #22C55E;
        border-radius: 6px;
    }
    
    /* Labels */
    QLabel.title { font-size: 18pt; font-weight: bold; color: white; margin-bottom: 10px; }
    QLabel.subtitle { font-size: 12pt; color: #A0A0A0; }
    QLabel.clock { font-size: 9pt; color: #3B82F6; font-weight: bold; }
"""

# ----------- THREAD DE PROCESSAMENTO -----------
class ConverterThread(QThread):
    status_signal = pyqtSignal(object, str, str)
    progress_signal = pyqtSignal(bool)

    def __init__(self, input_file, output_file, format, list_item, mode):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.format = format
        self.list_item = list_item
        self.mode = mode

    def run(self):
        try:
            self.progress_signal.emit(True)
            self.status_signal.emit(self.list_item, f"⏳ Convertendo: {os.path.basename(self.input_file)}", "#FACC15")
            
            if self.mode == "audio":
                audio = AudioSegment.from_file(self.input_file)
                audio.export(self.output_file, format=self.format.lower())

            elif self.mode == "video":
                if self.format.lower() == "mp3":
                     command = ["ffmpeg", "-y", "-i", self.input_file, "-q:a", "0", "-map", "a", self.output_file]
                else:
                     command = ["ffmpeg", "-y", "-i", self.input_file, self.output_file]
                
                subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

            elif self.mode == "image":
                img = Image.open(self.input_file)
                if self.format.upper() in ["JPG", "JPEG"] and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                img.save(self.output_file, self.format.upper())

            self.status_signal.emit(self.list_item, f"✅ Sucesso: {os.path.basename(self.output_file)}", "#4ADE80")
        
        except Exception as e:
            print(f"Erro: {e}")
            self.status_signal.emit(self.list_item, f"❌ Erro: {os.path.basename(self.input_file)}", "#F87171")
        
        finally:
            self.progress_signal.emit(False)

# ----------- JANELA DE CONVERSÃO (BASE) -----------
class BaseConverterApp(QWidget):
    def __init__(self, title, formats, mode, filter_ext, icon_emoji):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(600, 500)
        self.mode = mode
        self.filter_ext = filter_ext
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)

        header_layout = QHBoxLayout()
        icon_lbl = QLabel(icon_emoji)
        icon_lbl.setStyleSheet("font-size: 40px; background: transparent;")
        title_lbl = QLabel(title)
        title_lbl.setProperty("class", "title")
        header_layout.addWidget(icon_lbl)
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        self.file_list = QListWidget()
        main_layout.addWidget(self.file_list)

        controls_layout = QHBoxLayout()
        self.select_button = QPushButton("📂 Selecionar Arquivos")
        self.select_button.setProperty("class", "action")
        self.select_button.setCursor(Qt.PointingHandCursor)
        self.select_button.clicked.connect(self.select_files)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(formats)
        self.format_combo.setFixedWidth(100)

        controls_layout.addWidget(self.select_button)
        controls_layout.addWidget(QLabel("Formato:"))
        controls_layout.addWidget(self.format_combo)
        main_layout.addLayout(controls_layout)

        self.convert_button = QPushButton("🚀 INICIAR CONVERSÃO")
        self.convert_button.setProperty("class", "action")
        self.convert_button.setStyleSheet("font-size: 12pt; padding: 15px; background-color: #22C55E;")
        self.convert_button.setCursor(Qt.PointingHandCursor)
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.start_conversion)
        main_layout.addWidget(self.convert_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)
        self.input_files = []
        self.threads = []
        self.active_threads = 0

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Selecione Arquivos", "", self.filter_ext)
        if files:
            self.input_files = files
            self.file_list.clear()
            for file in files:
                self.file_list.addItem(f"📄 {os.path.basename(file)}")
            self.convert_button.setEnabled(True)
            self.progress_bar.setValue(0)
            self.convert_button.setText(f"🚀 INICIAR CONVERSÃO ({len(files)})")

    def update_item_status(self, item, text, color):
        item.setText(text)
        item.setForeground(QColor(color))

    def update_progress(self, is_running):
        if is_running:
            self.active_threads += 1
            self.progress_bar.setRange(0, 0) 
            self.convert_button.setEnabled(False)
            self.convert_button.setText("Processando... Aguarde")
            self.convert_button.setStyleSheet("background-color: #EAB308; color: black; font-weight: bold;")
        else:
            self.active_threads -= 1
            if self.active_threads == 0:
                self.progress_bar.setRange(0, 100)
                self.progress_bar.setValue(100)
                self.convert_button.setEnabled(True)
                self.convert_button.setText("Concluído! Converter Mais?")
                self.convert_button.setStyleSheet("background-color: #22C55E; color: white;")

    def start_conversion(self):
        fmt = self.format_combo.currentText()
        self.threads.clear()
        
        for i, file in enumerate(self.input_files):
            base, _ = os.path.splitext(file)
            output_file = f"{base}_convertido.{fmt.lower()}"
            item = self.file_list.item(i)
            
            thread = ConverterThread(file, output_file, fmt, item, self.mode)
            thread.status_signal.connect(self.update_item_status)
            thread.progress_signal.connect(self.update_progress)
            self.threads.append(thread)
            thread.start()

# ----------- MENU PRINCIPAL (DASHBOARD) -----------
class MainWindow(QMainWindow):
    def __init__(self, user_name="Usuário"):
        super().__init__()
        self.setWindowTitle("Multi Conversor Pro")
        self.resize(700, 500)
        self.setStyleSheet(STYLE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Título Personalizado
        lbl_title = QLabel(f"Olá, {user_name}! 👋")
        lbl_title.setProperty("class", "title")
        lbl_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_title)

        lbl_sub = QLabel("O que vamos converter hoje?")
        lbl_sub.setProperty("class", "subtitle")
        lbl_sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_sub)

        # Grid de Tiles
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(20)
        
        self.btn_audio = self.create_tile("🎵\nÁudio", "MP3, WAV, FLAC")
        self.btn_audio.clicked.connect(lambda: self.open_window("audio"))
        
        self.btn_video = self.create_tile("🎬\nVídeo", "MP4, AVI, MOV")
        self.btn_video.clicked.connect(lambda: self.open_window("video"))
        
        self.btn_image = self.create_tile("🖼️\nImagem", "JPG, PNG, BMP")
        self.btn_image.clicked.connect(lambda: self.open_window("image"))

        grid_layout.addWidget(self.btn_audio)
        grid_layout.addWidget(self.btn_video)
        grid_layout.addWidget(self.btn_image)

        layout.addLayout(grid_layout)
        layout.addStretch()

        # Rodapé
        lbl_footer = QLabel("Desenvolvido por Daniel Boechat")
        lbl_footer.setStyleSheet("color: #555; font-size: 8pt;")
        lbl_footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_footer)

        # Relógio
        self.lbl_clock = QLabel()
        self.lbl_clock.setProperty("class", "clock")
        self.lbl_clock.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_clock)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()

        self.current_window = None

    def update_clock(self):
        now = QDateTime.currentDateTime()
        locale = QLocale(QLocale.Portuguese, QLocale.Brazil)
        formatted_date = locale.toString(now, "dddd, d 'de' MMMM 'de' yyyy\nHH:mm:ss")
        formatted_date = formatted_date[0].upper() + formatted_date[1:]
        self.lbl_clock.setText(formatted_date)

    def create_tile(self, text, subtext):
        btn = QPushButton(f"{text}\n\n{subtext}")
        btn.setProperty("class", "tile")
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFixedSize(180, 180)
        return btn

    def open_window(self, type):
        if type == "audio":
            self.current_window = BaseConverterApp("Conversor de Áudio", ["MP3", "WAV", "FLAC", "OGG"], "audio", "Áudio (*.mp3 *.wav *.flac *.ogg)", "🎵")
        elif type == "video":
            self.current_window = BaseConverterApp("Conversor de Vídeo", ["AVI", "MP4", "MKV", "MP3"], "video", "Vídeo (*.mp4 *.avi *.mov *.mkv)", "🎬")
        elif type == "image":
            self.current_window = BaseConverterApp("Conversor de Imagem", ["JPG", "PNG", "BMP", "ICO"], "image", "Imagem (*.png *.jpg *.bmp *.gif)", "🖼️")
        self.current_window.show()

# ----------- STARTUP -----------
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except FileNotFoundError:
        if os.path.exists(os.path.join(FFMPEG_BIN, "ffmpeg.exe")): return True
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 

    # --- LÓGICA DO ÍCONE (FAVICON PNG) ---
    # Procura a pasta img de forma segura para o EXE
    img_folder = resource_path("img")
    
    # Tenta achar o primeiro PNG na pasta
    if os.path.exists(img_folder):
        found_icon = False
        for file in os.listdir(img_folder):
            if file.lower().endswith(".png"):
                full_path = os.path.join(img_folder, file)
                app.setWindowIcon(QIcon(full_path)) # Aplica em TODAS as janelas do app
                found_icon = True
                break
        if not found_icon:
            print("Nenhum PNG encontrado na pasta img")
    else:
        print(f"Pasta img não encontrada em: {img_folder}")

    # --- PERGUNTA O NOME ---
    user_name = "Usuário"
    input_dialog_style = """
        QDialog { background-color: #121212; color: white; }
        QLabel { color: white; font-size: 11pt; }
        QLineEdit { background-color: #1E1E1E; color: white; border: 1px solid #333; padding: 5px; }
        QPushButton { background-color: #3B82F6; color: white; border-radius: 5px; padding: 5px 15px; }
    """
    
    input_dialog = QInputDialog()
    input_dialog.setStyleSheet(input_dialog_style)
    input_dialog.setWindowTitle("Bem-vindo")
    input_dialog.setLabelText("Olá! Como você gostaria de ser chamado?")
    input_dialog.setInputMode(QInputDialog.TextInput)
    input_dialog.setOkButtonText("Entrar")
    input_dialog.setCancelButtonText("Pular")
    
    if input_dialog.exec_():
        text = input_dialog.textValue()
        if text.strip():
            user_name = text.strip()

    win = MainWindow(user_name)
    win.show()
    sys.exit(app.exec_())