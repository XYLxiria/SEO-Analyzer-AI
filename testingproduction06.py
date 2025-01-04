import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QPlainTextEdit, QFileDialog, QMessageBox, QAction, QMenuBar, QMenu, QToolBar, QMainWindow
from PyQt5.QtGui import QFont, QPixmap, QTextCursor, QIcon
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer, QDateTime
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from collections import Counter
import re
import pickle
import os

pickle_path = 'stopwords.pkl'

if os.path.exists(pickle_path):
    with open(pickle_path, 'rb') as f:
        stop_words = pickle.load(f)
else:
    stop_words = set(stopwords.words('english')).union(set(stopwords.words('indonesian')))
    with open(pickle_path, 'wb') as f:
        pickle.dump(stop_words, f)

nltk.data.path.append('Z:\\SKRIPSI\\SEOChecker\\nltk_data')
stop_words = set(stopwords.words('english')).union(set(stopwords.words('indonesian')))

class AnalysisThread(QThread):
    analysis_complete = pyqtSignal(str, list, list, list, list, bytes, int, dict)

    def __init__(self, url):
        super(AnalysisThread, self).__init__()
        self.url = url

    def run(self):
        good = []
        bad = []
        title_message = ""
        description_message = ""
        image_count = 0
        additional_analysis = {}
        
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            self.analysis_complete.emit("Error: Permintaan waktu habis (timeout). Silakan coba lagi.", [], [], [], [], b'', [], 0, {})
            return
        except requests.exceptions.RequestException as e:
            self.analysis_complete.emit(f"Error: {str(e)}", [], [], [], [], b'', 0, {})
            return

        if response.status_code != 200:
            self.analysis_complete.emit("Error: Tidak bisa mengakses website untuk analisa.", [], [], [], [], b'', [], 0, {})
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').get_text() if soup.find('title') else None
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None

        if title:
            title_message = f"{title}"
        else:
            title_message = "Judul Web tidak ditemukan, tolong berikan judul laman nya"

        if description:
            description_message = f"{description}"
        else:
            description_message = "Deskripsi Web tidak ditemukan, tolong minta administrator / pengembang untuk menambahkan deskripsi meta nya"

        hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        h_tags = []
        for h in soup.find_all(hs):
            good.append(f"{h.name}-->{h.text.strip()}")
            h_tags.append(h.name)

        if 'h1' not in h_tags:
            bad.append("Tidak ditemukan header H1!")

        for img in soup.find_all('img'):
            image_count += 1
            if not img.get('alt'):
                bad.append(f"Image tanpa alt: {img}")

        additional_analysis['heading_tags'] = {tag: h_tags.count(tag) for tag in hs}
        additional_analysis['meta_description_length'] = len(description) if description else 0

        keywords = self.extract_keywords(soup)
        additional_chart_data = self.additional_chart_analysis(soup)

        self.analysis_complete.emit(
            f"Analisa Komplit, Website yang dianalisa : {self.url}",
            [title_message, description_message],
            keywords,
            good,
            bad,
            additional_chart_data,
            image_count,
            additional_analysis
        )

    def extract_keywords(self, soup):
        paragraphs = soup.find_all('p')
        text_content = ' '.join([paragraph.text for paragraph in paragraphs])
        words = nltk.word_tokenize(text_content)
        filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]
        freq = nltk.FreqDist(filtered_words)
        keywords = freq.most_common(10)
        return keywords

    def additional_chart_analysis(self, soup):
        paragraphs = soup.find_all('p')
        text_content = ' '.join([paragraph.text for paragraph in paragraphs])
        vectorizer = CountVectorizer(stop_words=list(stop_words))
        try:
            word_frequencies = vectorizer.fit_transform([text_content])
            if word_frequencies.shape[1] == 0:
                raise ValueError("Vocabulary kosong, mungkin semua kata hanya berupa sesuatu yang tidak spesifik")
            
            feature_names = vectorizer.get_feature_names_out()
            total_word_frequencies = word_frequencies.sum(axis=0).A1
            word_freq_pairs = list(zip(feature_names, total_word_frequencies))
            word_freq_pairs = sorted(word_freq_pairs, key=lambda x: x[1], reverse=True)[:30]
            top_words, top_frequencies = zip(*word_freq_pairs)
        except ValueError as e:
            print(f"Error: {str(e)}")
            return b''

        screen_size = QApplication.primaryScreen().size()
        width = int(screen_size.width() * 0.75)
        height = int(screen_size.height() * 0.75)
        plt.figure(figsize=(width / 100, height / 100))
        plt.bar(top_words, top_frequencies)
        plt.xticks(rotation='vertical')
        plt.xlabel('Kata Kunci')
        plt.ylabel('Frekuensi Kata Kunci')
        plt.title('Kata Kunci Terbanyak Dalam Website (Top 30)')
        plt.tight_layout()

        chart_image_bytes = BytesIO()
        plt.savefig(chart_image_bytes, format='png')
        plt.close()

        return chart_image_bytes.getvalue()

class SEOAnalyzerApp(QMainWindow):
    def __init__(self):
        super(SEOAnalyzerApp, self).__init__()
        self.setWindowIcon(QIcon('icon.png'))
        self.history = []
        self.init_ui()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.showMinimized()
        elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.start_analysis()
        else:
            super(SEOAnalyzerApp, self).keyPressEvent(event)


    def init_ui(self):
        main_layout = QVBoxLayout()

        url_label = QLabel("Masukkan URL Website :")
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://contoh.com")
        self.url_input.setFont(QFont("Arial", 12))
        main_layout.addWidget(url_label)
        main_layout.addWidget(self.url_input)

        analyze_button = QPushButton("Mulai Analisa", self)
        analyze_button.setFont(QFont("Arial", 12))
        analyze_button.clicked.connect(self.start_analysis)
        main_layout.addWidget(analyze_button)

        self.progress_bar = QProgressBar(self)
        main_layout.addWidget(self.progress_bar)

        analysis_boxes_layout = QHBoxLayout()

        self.first_analysis_box = QPlainTextEdit(self)
        self.first_analysis_box.setReadOnly(True)
        self.first_analysis_box.setFont(QFont("Courier New", 10))
        analysis_boxes_layout.addWidget(self.first_analysis_box)

        self.second_analysis_box = QPlainTextEdit(self)
        self.second_analysis_box.setReadOnly(True)
        self.second_analysis_box.setFont(QFont("Courier New", 10))
        analysis_boxes_layout.addWidget(self.second_analysis_box)

        main_layout.addLayout(analysis_boxes_layout)

        self.third_analysis_box = QPlainTextEdit(self)
        self.third_analysis_box.setReadOnly(True)
        self.third_analysis_box.setFont(QFont("Courier New", 12))
        main_layout.addWidget(self.third_analysis_box)

        show_chart_button = QPushButton("Tampilkan Analisa Diagram", self)
        show_chart_button.setFont(QFont("Arial", 12))
        show_chart_button.clicked.connect(self.show_chart_window)
        main_layout.addWidget(show_chart_button)

        save_pdf_button = QPushButton("Simpan ke PDF", self)
        save_pdf_button.setFont(QFont("Arial", 12))
        save_pdf_button.clicked.connect(self.save_to_pdf)
        main_layout.addWidget(save_pdf_button)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        
        self.setCentralWidget(central_widget)

        self.create_menu_bar()
        self.setWindowTitle("Aplikasi Analisis SEO")
        self.setWindowIcon(QIcon('icon.png'))
        screen_size = QApplication.primaryScreen().size()
        width = int(screen_size.width() * 0.90)
        height = int(screen_size.height() * 0.90)
        self.resize(width, height)

        self.analysis_thread = None
        self.chart_window = None
    
    def create_menu_bar(self):
        menubar = self.menuBar()

        history_menu = menubar.addMenu('Riwayat')
        history_action = QAction('Riwayat Analisa', self)
        history_action.triggered.connect(self.show_history)
        history_menu.addAction(history_action)
        clear_history_action = QAction('Hapus Riwayat', self)
        clear_history_action.triggered.connect(self.clear_history)
        history_menu.addAction(clear_history_action)

        about_menu = menubar.addMenu('Detail')
        about_action = QAction('Tentang Aplikasi', self)
        about_action.triggered.connect(self.show_about_dialog)
        about_menu.addAction(about_action)
        feature_action = QAction('Fitur', self)
        feature_action.triggered.connect(self.show_feature)
        about_menu.addAction(feature_action)

    def show_history(self):
        if not self.history:
            self.show_message("Tidak ada riwayat ditemukan.") 
            return

        history_text = '\n'.join([f"{url} - {timestamp}" for url, timestamp in self.history])
        self.show_message(f"URL yang dianalisa:\n{history_text}")
    
    def clear_history(self):
        self.history.clear()
        self.show_message("Riwayat dibersihkan.")
    
    def show_about_dialog(self):
        about_text = (
    "Aplikasi ini dibuat oleh Isvandika Adisana untuk kebutuhan skripsi\n\n"
    "Aplikasi ini dapat digunakan untuk menganalisis SEO dari sebuah website. "
    "Aplikasi ini menggunakan Python, PyQt5, BeautifulSoup, NLTK, dan Matplotlib.\n\n"
    "Anda menggunakan versi 2.0\n"
    "Aplikasi ini berada di bawah lisensi MIT-License"
)
        self.show_message(about_text)
    
    def show_feature(self):
        about_text = (
    "Anda bisa menggunakan tombol ESC untuk minimalkan jendela\n\n"
    "Anda bisa menekan tombol Enter atau Return untuk memulai analisis\n\n"
    "Anda juga bisa menyimpan hasil analisa sebagai PDF\n\n"
    "Untuk fitur lebih lanjut, akan selalu di-update untuk kedepannya"
)
        self.show_message(about_text)
    
    def show_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle("Informasi")
        msg.exec_()

    def start_analysis(self):
        self.first_analysis_box.clear()
        self.second_analysis_box.clear()
        self.third_analysis_box.clear()

        url = self.url_input.text()

        current_datetime = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm:ss")

        self.history.append((url, current_datetime))

        regex = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE)

        if not re.match(regex, url):
            self.show_message("URL tidak valid. Pastikan URL yang dimasukkan benar.")
            return

        self.analysis_thread = AnalysisThread(url)
        self.analysis_thread.analysis_complete.connect(self.display_results)
        self.analysis_thread.start()

        self.progress_bar.setRange(0, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(10000)

    def on_timeout(self):
        if self.analysis_thread.isRunning():
            self.analysis_thread.terminate() 
            self.display_results("Error: Analisis waktu habis. Silakan coba lagi.", [], [], [], [], b'', [], 0, {})

    def add_horizontal_line(self, widget):
        width = widget.viewport().width()
        font_metrics = widget.fontMetrics()
        char_width = font_metrics.horizontalAdvance('-')
        num_chars = width // char_width
        if num_chars > 0:
            num_chars -= 3
        widget.appendPlainText("\n" + "-" * num_chars + "\n")

    def display_results(self, message, title_description, keywords, good, bad, chart_image_bytes, image_count, additional_analysis, num_results=0, extra_info={}):
        self.first_analysis_box.clear()
        self.first_analysis_box.appendPlainText(message)
        if title_description:
            title = title_description[0] if len(title_description) > 0 else None
            description = title_description[1] if len(title_description) > 1 else None

            if title:
                self.first_analysis_box.appendPlainText(f"Judul Web : {title}")
            else:
                self.first_analysis_box.appendPlainText("Judul Web tidak ditemukan, tolong berikan judul laman nya")

            if description:
                self.first_analysis_box.appendPlainText(f"Deskripsi Web : {description}")
            else:
                self.first_analysis_box.appendPlainText("Deskripsi Web tidak ditemukan, tolong tambah deskripsi meta nya")
        else:
            self.first_analysis_box.appendPlainText("Tidak ada informasi judul dan deskripsi yang ditemukan.")
        self.first_analysis_box.moveCursor(QTextCursor.Start)

        self.second_analysis_box.clear()
        self.second_analysis_box.appendPlainText("Kata Kunci Utama (Top 10):\n")
        for keyword, freq in keywords:
            self.second_analysis_box.appendPlainText(f"{keyword}: {freq}")
        self.second_analysis_box.moveCursor(QTextCursor.Start)

        self.third_analysis_box.clear()
        self.third_analysis_box.appendPlainText("Analisis Tambahan :")
        self.add_horizontal_line(self.third_analysis_box)

        if isinstance(additional_analysis, dict):
            if 'meta_description_length' in additional_analysis:
                self.third_analysis_box.appendPlainText(f"Panjang Meta Description: {additional_analysis['meta_description_length']} karakter")
            self.add_horizontal_line(self.third_analysis_box)

            if 'heading_tags' in additional_analysis:
                self.third_analysis_box.appendPlainText("Jumlah Heading Tags:\n")
                for tag, count in additional_analysis['heading_tags'].items():
                    self.third_analysis_box.appendPlainText(f"{tag}: {count}")
                self.add_horizontal_line(self.third_analysis_box)
        else:
            self.third_analysis_box.appendPlainText("Error: additional_analysis is not a dictionary.")
            self.add_horizontal_line(self.third_analysis_box)

        self.third_analysis_box.appendPlainText("Judul Header Yang Ditemukan :\n")
        for item in good:
            self.third_analysis_box.appendPlainText(f"{item}")
        self.add_horizontal_line(self.third_analysis_box)

        self.third_analysis_box.appendPlainText(f"Total jumlah gambar yang terdeteksi pada laman ini : {image_count}\n")
        self.third_analysis_box.appendPlainText("Perbaikan pada tag 'Alt' gambar yang diperlukan:\n")
        for item in bad:
            img_src = re.search(r'src="([^"]+)"', item)
            img_link = img_src.group(1) if img_src else "Tidak ditemukan"
            self.third_analysis_box.appendPlainText(f"- Image tanpa alt pada link = \"{img_link}\" ")

        self.third_analysis_box.moveCursor(QTextCursor.Start)

        self.chart_image_bytes = chart_image_bytes

        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.timer.stop()

    def show_chart_window(self):
        if not self.chart_image_bytes:
            return
        if self.chart_window:
            self.chart_window.close()
        self.chart_window = QWidget()
        self.chart_window.setWindowTitle("Analisa Diagram")
        layout = QVBoxLayout()
        chart_label = QLabel(self.chart_window)
        pixmap = QPixmap()
        pixmap.loadFromData(self.chart_image_bytes)
        chart_label.setPixmap(pixmap)
        layout.addWidget(chart_label)
        self.chart_window.setLayout(layout)
        self.chart_window.show()


    def save_to_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Simpan sebagai PDF", "", "PDF Files (*.pdf)")
        if not file_path:
            return

        doc = SimpleDocTemplate(file_path, pagesize=letter, title=f"Hasil Analisa {self.url_input.text()}")
        styles = getSampleStyleSheet()

        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=12,
            leading=18,
        )
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Normal'],
            fontName='Times-Bold',
            fontSize=14,
            leading=21,
            spaceAfter=12,
        )

        content = []

        def clean_html(text):
            clean = re.compile(r'<(?!br\s*/?)[^>]+>')
            return re.sub(clean, '', text)

        def add_text_with_newline(text, style):
            text = re.sub(r"\n-+\n", "\n", text)
            for line in text.split('\n'):
                clean_line = re.sub(r"^[-]+$", "", line).strip()
                clean_line = re.sub(r"Image tanpa alt:.*", "", line).strip()
                content.append(Paragraph(clean_line, style))
                content.append(Spacer(1, 6))

        def add_pdf_separator_line(content):
            line = HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black, spaceBefore=0.5 * inch, spaceAfter=0.5 * inch)
            content.append(line)

        first_analysis_text = clean_html(self.first_analysis_box.toPlainText())
        second_analysis_text = clean_html(self.second_analysis_box.toPlainText())
        third_analysis_text = clean_html(self.third_analysis_box.toPlainText())

        content.append(Paragraph("Hasil Analisis:", title_style))
        content.append(Spacer(1, 12))

        sections = [
            ("Keterangan Web Yang Dianalisa", first_analysis_text),
            ("Kata Kunci Paling Sering Digunakan", second_analysis_text),
            ("Beberapa Bagian Yang Perlu Diperbaiki", third_analysis_text),
        ]

        for title, text in sections:
            content.append(Paragraph(title, title_style))
            add_text_with_newline(text, normal_style)
            add_pdf_separator_line(content)

        if self.chart_image_bytes:
            content.append(Paragraph("Analisa Diagram", title_style))
            chart_image = Image(BytesIO(self.chart_image_bytes))
            chart_image.drawHeight = 3 * inch
            chart_image.drawWidth = 6 * inch
            content.append(chart_image)

        doc.build(content)
        self.show_message("PDF berhasil disimpan.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = SEOAnalyzerApp()
    main_app.showMaximized()
    main_window=QMainWindow()
    main_window.setWindowIcon(QIcon('Assets/favicon.ico'))
    sys.exit(app.exec_())