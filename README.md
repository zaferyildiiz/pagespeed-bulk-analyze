# 🚀 PageSpeed Bulk Analyzer

A lightweight Flask-based tool to **analyze multiple URLs** using Google PageSpeed Insights API – perfect for SEO specialists and web developers!  
Run it locally and get insights on **performance**, **accessibility**, **best practices**, and more.

---

## 📦 Features

- ✅ Bulk PageSpeed Insights analysis (desktop & mobile)  
- ✅ Simple web interface  
- ✅ Lightweight & fast (Flask backend)  
- ✅ Export results as JSON or CSV (planned)  
- ✅ Docker support 🐳

---

## 🧪 Demo Screenshot

> 🖼️ Add a screenshot of the app here if you want

---

## ⚙️ Requirements

Python 3.8+ Flask 3.x requests

yaml 

---

## 🐳 Run with Docker (recommended)

Build Docker image
docker build -t pagespeed-app .

Run the container
docker run -p 5000:5000 pagespeed-app

yaml 

Then open 👉 http://localhost:5000 in your browser.

---

## 💻 Run Locally (Dev Mode)

Create virtual environment (optional but recommended)
python3 -m venv venv source venv/bin/activate

Install requirements
pip install -r requirements.txt

Run the app
python app.py

yaml 

---

## 📝 TODO

- [x] Basic input & output interface  
- [ ] CSV export  
- [ ] Improve error handling  
- [ ] Add page score color indicators (green/yellow/red)

---

## 📄 License

MIT © [Zafer Yıldız](https://github.com/zaferyildiiz)
