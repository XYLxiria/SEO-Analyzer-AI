import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QPlainTextEdit, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap, QKeySequence
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QTimer
import requests
from bs4 import BeautifulSoup
import nltk
import spacy
import spacy.cli
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from io import BytesIO
from spacy import displacy

try:
    spacy.cli.download("en_core_web_sm")
except Exception as e:
    print("Error during model download:", e)
nlp = spacy.load("en_core_web_sm")

class AnalysisThread(QThread):
    analysis_complete = pyqtSignal(str, list, list, list, list, bytes, list)

    def __init__(self, url):
        super(AnalysisThread, self).__init__()
        self.url = url

    def run(self):
        good = []
        bad = []

        try:
            response = requests.get(self.url, timeout=10)
        except requests.exceptions.Timeout:
            self.analysis_complete.emit("Error: Permintaan waktu habis (timeout). Silakan coba lagi.", [], [], [], [], b'', [])
            return
        except requests.exceptions.RequestException as e:
            self.analysis_complete.emit(f"Error: {str(e)}", [], [], [], [], b'', [])
            return

        if response.status_code != 200:
            self.analysis_complete.emit("Error: Tidak bisa mengakses website untuk analisa.", [], [], [], [], b'', [])
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('title').get_text() if soup.find('title') else None
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None


        if title:
            good.append("Judul Ada! Ini Bagus!")
        else:
            bad.append("Judul Web tidak ditemukan, tolong berikan judul laman nya")

        if description:
            good.append("Deskripsi Web Ditemukan! Bagus!")
        else:
            bad.append("Deskripsi Web tidak ditemukan, tolong minta administrator / pengembang untuk menambahkan deskripsi meta nya")


        hs = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        h_tags = []
        for h in soup.find_all(hs):
            good.append(f"{h.name}-->{h.text.strip()}")
            h_tags.append(h.name)

        if 'h1' not in h_tags:
            bad.append("Tidak ditemukan header H1!")

 
        for i in soup.find_all('img', alt=''):
            bad.append(f"Tidak ditemukan Alt: {i}")

        keywords = self.extract_keywords(soup)

        additional_chart_data = self.additional_chart_analysis(soup)

        ner_entities = self.ner_analysis(soup)

        self.analysis_complete.emit(
            f"Analisa Komplit, Website yang dianalisa : {self.url}",
            [title, description],
            keywords,
            good,
            bad,
            additional_chart_data,
            ner_entities
        )

    def extract_keywords(self, soup):
        paragraphs = soup.find_all('p')
        text_content = ' '.join([paragraph.text for paragraph in paragraphs])

        words = nltk.word_tokenize(text_content)
        filtered_words = [word.lower() for word in words if word.isalpha()]

        freq = nltk.FreqDist(filtered_words)
        keywords = freq.most_common(10)

        return keywords

    def additional_chart_analysis(self, soup):
        paragraphs = soup.find_all('p')
        text_content = ' '.join([paragraph.text for paragraph in paragraphs])

        vectorizer = CountVectorizer()
        word_frequencies = vectorizer.fit_transform([text_content])

        feature_names = vectorizer.get_feature_names_out()

        total_word_frequencies = word_frequencies.sum(axis=0).A1

        word_freq_pairs = list(zip(feature_names, total_word_frequencies))

        word_freq_pairs = sorted(word_freq_pairs, key=lambda x: x[1], reverse=True)[:30]

        top_words, top_frequencies = zip(*word_freq_pairs)

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


    def ner_analysis(self, soup):
        text = ' '.join([paragraph.text for paragraph in soup.find_all('p')])

        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        return entities


class SEOAnalyzerApp(QWidget):
    def __init__(self):
        super(SEOAnalyzerApp, self).__init__()
        self.init_ui()

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

        show_ner_analysis_button = QPushButton("Tampilkan Analisa Lebih Spesifik", self)
        show_ner_analysis_button.setFont(QFont("Arial", 12))
        show_ner_analysis_button.clicked.connect(self.show_ner_analysis_window)
        main_layout.addWidget(show_ner_analysis_button)

        self.setLayout(main_layout)

        self.setWindowTitle("Aplikasi Analisis SEO")
        screen_size = QApplication.primaryScreen().size()
        width = int(screen_size.width() * 0.90)
        height = int(screen_size.height() * 0.90)
        self.resize(width, height)

        self.analysis_thread = None
        self.chart_window = None
        self.ner_analysis_window = None

    def start_analysis(self):
        self.first_analysis_box.clear()
        self.second_analysis_box.clear()
        self.third_analysis_box.clear()

        url = self.url_input.text()

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
            self.display_results("Error: Analisis waktu habis. Silakan coba lagi.", [], [], [], [], b'', [])

    def display_results(self, message, title_description, keywords, good, bad, chart_image_bytes, ner_entities):
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

        self.second_analysis_box.clear()
        self.second_analysis_box.appendPlainText("--- Kata Kunci Terbanyak---")
        for keyword in keywords:
            self.second_analysis_box.appendPlainText(f"{keyword[0]}: {keyword[1]}")

        self.third_analysis_box.clear()
        self.third_analysis_box.appendPlainText("\n--- Header Yang Ditemukan ---")
        for idx, item in enumerate(good, start=1):
            self.third_analysis_box.appendPlainText(f"{idx}. {item}")

        self.third_analysis_box.appendPlainText("\n--- Deskripsi Alt yang tidak ditemukan ---")
        for idx, item in enumerate(bad, start=1):
            self.third_analysis_box.appendPlainText(f"{idx}. {item}")

        self.third_analysis_box.verticalScrollBar().setValue(0)

        self.progress_bar.setRange(0, 1)  

        self.chart_image_bytes = chart_image_bytes

        self.ner_entities = ner_entities

    def show_chart_window(self):
        if self.chart_window is not None and self.chart_window.isVisible():
            self.chart_window.close()

        self.chart_window = ChartWindow(self.chart_image_bytes)
        self.chart_window.setWindowTitle("Diagram Kata Kunci Terbanyak")
        self.chart_window.show()

    def show_ner_analysis_window(self):
        if self.ner_analysis_window is not None and self.ner_analysis_window.isVisible():
            self.ner_analysis_window.close()

        self.ner_analysis_window = ChartWindowNER(self.ner_entities)
        self.ner_analysis_window.setWindowTitle("Analisis NER")
        self.ner_analysis_window.show()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F4 and event.modifiers() & Qt.AltModifier:
            self.close()
        else:
            super().keyPressEvent(event)


class ChartWindow(QWidget):
    def __init__(self, chart_image_bytes):
        super().__init__()
        self.init_ui()
        self.set_chart(chart_image_bytes)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.chart_label = QLabel(self)
        layout.addWidget(self.chart_label)

    def set_chart(self, chart_image_bytes):
        chart_pixmap = QPixmap()
        chart_pixmap.loadFromData(chart_image_bytes)
        self.chart_label.setPixmap(chart_pixmap)


class ChartWindowNER(QWidget):
    def __init__(self, ner_entities):
        super().__init__()
        self.init_ui()
        self.set_ner_analysis(ner_entities)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.ner_label = QLabel(self)
        layout.addWidget(self.ner_label)

    def set_ner_analysis(self, ner_entities):
        entity_counter = Counter([entity[0] for entity in ner_entities])
        entities, counts = zip(*entity_counter.items())

        if len(entities) > 20:
            entities = entities[:20]
            counts = counts[:20]

        fig, ax = plt.subplots()
        ax.barh(entities, counts, color='skyblue')
        ax.set_xlabel('Jumlah Kemunculan')
        ax.set_ylabel('Entitas')
        ax.set_title('Analisis NER (Top 20)')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        plt.tight_layout()

        chart_image_bytes = BytesIO()
        plt.savefig(chart_image_bytes, format='png')
        plt.close()

        chart_pixmap = QPixmap()
        chart_pixmap.loadFromData(chart_image_bytes.getvalue())
        self.ner_label.setPixmap(chart_pixmap)

def main():
    app = QApplication(sys.argv)
    window = SEOAnalyzerApp()
    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()