import os
import nltk

nltk_data_dir = os.path.join("Z:", "SKRIPSI", "SEOChecker", "nltk_data")

stopwords_dir = os.path.join(nltk_data_dir, "corpora", "stopwords")
punkt_dir = os.path.join(nltk_data_dir, "tokenizers", "punkt")

os.makedirs(stopwords_dir, exist_ok=True)
os.makedirs(punkt_dir, exist_ok=True)

nltk.download("stopwords", download_dir=stopwords_dir)
nltk.download("punkt", download_dir=punkt_dir)

print("berhasil dan disimpan pada:", nltk_data_dir)
