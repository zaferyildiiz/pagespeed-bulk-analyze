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

> 🖼️ *(Add a screenshot of the app here if you'd like)*

---

## ⚙️ Requirements

Python 3.8+ Flask 3.x requests
 

---

## 🐳 Run with Docker (Recommended)

> Make sure you have [Docker installed](https://docs.docker.com/get-docker/) on your system.

### 🔧 Build the Docker image:

```bash
docker build -t pagespeed-app .
▶️ Run the container:
bash 
docker run -p 5000:5000 pagespeed-app
The app will be accessible at 👉 http://localhost:5000

💻 Run Locally (Development)
For Python environments (without Docker)

 
# Clone the repository
git clone https://github.com/zaferyildiiz/pagespeed-bulk-analyze.git
cd pagespeed-bulk-analyze

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask app
python app.py
📝 TODO
 Basic input & output interface

 CSV export

 Improve error handling

 Add page score color indicators (green/yellow/red)

📄 License
MIT © Zafer Yıldız
