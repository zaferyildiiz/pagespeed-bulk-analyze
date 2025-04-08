from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# HTML şablonu burada inline olarak tanımlanır
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PageSpeed API Analiz Aracı</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- SheetJS ve FileSaver.js kütüphanelerini ekle -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
    <style>
        .score-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin: 0 auto;
            color: white;
        }
        .score-good {
            background-color: #0cce6b;
        }
        .score-average {
            background-color: #ffa400;
        }
        .score-poor {
            background-color: #ff4e42;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(0, 0, 0, 0.1);
            border-radius: 50%;
            border-top-color: #333;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center mb-4">PageSpeed API Analiz Aracı</h1>
        
        <div class="row mb-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">URL'leri Girin</h5>
                        <div class="form-group">
                            <textarea id="urlInput" class="form-control" rows="5" placeholder="Her satıra bir URL girin (örn: https://example.com)"></textarea>
                        </div>
                        <div class="d-flex justify-content-between mt-3">
                            <button id="analyzeButton" class="btn btn-primary">Analize Başla</button>
                            <button id="downloadExcelButton" class="btn btn-success" disabled>Excel İndir</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Analiz Sonuçları</h5>
                        <div class="table-responsive">
                            <table class="table table-striped" id="resultsTable">
                                <thead>
                                    <tr>
                                        <th>URL</th>
                                        <th>Performance (Masaüstü)</th>
                                        <th>Accessibility (Masaüstü)</th>
                                        <th>Best Practices (Masaüstü)</th>
                                        <th>SEO (Masaüstü)</th>
                                        <th>Performance (Mobil)</th>
                                        <th>Accessibility (Mobil)</th>
                                        <th>Best Practices (Mobil)</th>
                                        <th>SEO (Mobil)</th>
                                    </tr>
                                </thead>
                                <tbody id="resultsBody"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const analyzeButton = document.getElementById('analyzeButton');
            const downloadExcelButton = document.getElementById('downloadExcelButton');
            const urlInput = document.getElementById('urlInput');
            const resultsBody = document.getElementById('resultsBody');
            
            // Sonuçları saklayacak global değişken
            let allResults = [];
            
            analyzeButton.addEventListener('click', function() {
                const urls = urlInput.value.trim().split('\\n').filter(url => url.trim() !== '');
                
                if (urls.length === 0) {
                    alert('Lütfen en az bir URL girin.');
                    return;
                }
                
                // Sonuçları sıfırla ve Excel indirme butonunu devre dışı bırak
                allResults = [];
                downloadExcelButton.disabled = true;
                
                // Tabloyu temizle
                resultsBody.innerHTML = '';
                
                // Tüm URL'ler için sıralarını koruyarak satır ekle
                urls.forEach((url, index) => {
                    const row = document.createElement('tr');
                    row.id = `result-row-${index}`;
                    row.innerHTML = `
                        <td>${url}</td>
                        <td><div class="loading"></div></td>
                        <td><div class="loading"></div></td>
                        <td><div class="loading"></div></td>
                        <td><div class="loading"></div></td>
                        <td><div class="loading"></div></td>
                        <td><div class="loading"></div></td>
                        <td><div class="loading"></div></td>
                        <td><div class="loading"></div></td>
                    `;
                    resultsBody.appendChild(row);
                });
                
                // Her URL için sırayla analiz yap (ardışık değil, biri bitince diğerine geçmeyi beklemeden)
                urls.forEach((url, index) => {
                    analyzeUrl(url, index);
                });
            });
            
            function analyzeUrl(url, index) {
                // Masaüstü ve mobil analizleri için Promise dizisi oluştur
                Promise.all([
                    // Masaüstü analizi
                    fetch('/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ url, strategy: 'desktop' }),
                    }).then(response => {
                        if (!response.ok) {
                            throw new Error('Masaüstü API isteği başarısız');
                        }
                        return response.json();
                    }),
                    
                    // Mobil analizi
                    fetch('/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ url, strategy: 'mobile' }),
                    }).then(response => {
                        if (!response.ok) {
                            throw new Error('Mobil API isteği başarısız');
                        }
                        return response.json();
                    })
                ])
                .then(([desktopData, mobileData]) => {
                    // Sonuçları global değişkene ekle
                    allResults[index] = {
                        url: url,
                        desktop_performance: desktopData.performance,
                        desktop_accessibility: desktopData.accessibility,
                        desktop_best_practices: desktopData.best_practices,
                        desktop_seo: desktopData.seo,
                        mobile_performance: mobileData.performance,
                        mobile_accessibility: mobileData.accessibility,
                        mobile_best_practices: mobileData.best_practices,
                        mobile_seo: mobileData.seo
                    };
                    
                    // Her iki analiz de tamamlandığında sonuçları güncelle
                    updateResultRow(url, desktopData, mobileData, index);
                    
                    // Hiç sonuç yoksa Excel indirme butonunu aktif et
                    if (allResults.filter(r => r !== undefined).length > 0) {
                        downloadExcelButton.disabled = false;
                    }
                })
                .catch(error => {
                    console.error('Hata:', error);
                    updateResultRowWithError(url, index);
                });
            }
            
            function getScoreClass(score) {
                if (score >= 90) return 'score-good';
                if (score >= 50) return 'score-average';
                return 'score-poor';
            }
            
            function updateResultRow(url, desktopData, mobileData, index) {
                const row = document.getElementById(`result-row-${index}`);
                if (row) {
                    row.innerHTML = `
                        <td>${url}</td>
                        
                        <!-- Masaüstü sonuçları -->
                        <td>
                            <div class="score-circle ${getScoreClass(desktopData.performance)}">${desktopData.performance}</div>
                        </td>
                        <td>
                            <div class="score-circle ${getScoreClass(desktopData.accessibility)}">${desktopData.accessibility}</div>
                        </td>
                        <td>
                            <div class="score-circle ${getScoreClass(desktopData.best_practices)}">${desktopData.best_practices}</div>
                        </td>
                        <td>
                            <div class="score-circle ${getScoreClass(desktopData.seo)}">${desktopData.seo}</div>
                        </td>
                        
                        <!-- Mobil sonuçları -->
                        <td>
                            <div class="score-circle ${getScoreClass(mobileData.performance)}">${mobileData.performance}</div>
                        </td>
                        <td>
                            <div class="score-circle ${getScoreClass(mobileData.accessibility)}">${mobileData.accessibility}</div>
                        </td>
                        <td>
                            <div class="score-circle ${getScoreClass(mobileData.best_practices)}">${mobileData.best_practices}</div>
                        </td>
                        <td>
                            <div class="score-circle ${getScoreClass(mobileData.seo)}">${mobileData.seo}</div>
                        </td>
                    `;
                }
            }
            
            function updateResultRowWithError(url, index) {
                const row = document.getElementById(`result-row-${index}`);
                if (row) {
                    row.innerHTML = `
                        <td>${url}</td>
                        <td colspan="8" class="text-center text-danger">Analiz sırasında hata oluştu</td>
                    `;
                }
            }
            
            // Excel indirme fonksiyonu
            downloadExcelButton.addEventListener('click', function() {
                if (allResults.length === 0) {
                    alert('İndirilecek veri bulunmamaktadır.');
                    return;
                }
                
                // Boş satırları filtrele
                const filteredResults = allResults.filter(result => result !== undefined);
                
                // Excel dosyasını oluştur
                const worksheet = XLSX.utils.json_to_sheet(filteredResults);
                
                // Kolon genişliklerini ayarla
                const wscols = [
                    {wch: 40}, // URL
                    {wch: 15}, // Masaüstü Performance
                    {wch: 15}, // Masaüstü Accessibility
                    {wch: 15}, // Masaüstü Best Practices
                    {wch: 15}, // Masaüstü SEO
                    {wch: 15}, // Mobil Performance
                    {wch: 15}, // Mobil Accessibility
                    {wch: 15}, // Mobil Best Practices
                    {wch: 15}  // Mobil SEO
                ];
                
                worksheet['!cols'] = wscols;
                
                // Başlıkları belirt
                XLSX.utils.sheet_add_aoa(worksheet, [['URL', 
                    'Performance (Masaüstü)', 'Accessibility (Masaüstü)', 'Best Practices (Masaüstü)', 'SEO (Masaüstü)',
                    'Performance (Mobil)', 'Accessibility (Mobil)', 'Best Practices (Mobil)', 'SEO (Mobil)'
                ]], {origin: 'A1'});
                
                const workbook = XLSX.utils.book_new();
                XLSX.utils.book_append_sheet(workbook, worksheet, 'PageSpeed Sonuçları');
                
                // Excel dosyasını indir
                const date = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
                XLSX.writeFile(workbook, `pagespeed-raporu-${date}.xlsx`);
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    strategy = data.get('strategy', 'desktop')  # Varsayılan olarak masaüstü
    
    if not url:
        return jsonify({"error": "URL gerekli"}), 400
    
    try:
        # API anahtarımızı buraya girelim
        API_KEY = "YOUR_API_KEY" 
        
        # PageSpeed API isteği - tüm kategorileri açıkça belirt ve strateji (masaüstü/mobil) parametresini ekle
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy={strategy}&category=PERFORMANCE&category=ACCESSIBILITY&category=BEST_PRACTICES&category=SEO"
        
        # API anahtarı varsa ekle
        if API_KEY:
            api_url += f"&key={API_KEY}"
            
        response = requests.get(api_url)
        
        if response.status_code != 200:
            return jsonify({"error": f"API hatası: {response.status_code}"}), 500
        
        result = response.json()
        
        # DEbug yapıyorş
        print(f"API response for {url} ({strategy}):", result.keys())
        
        # Kategori
        categories = result.get('lighthouseResult', {}).get('categories', {})
        
        # Kategori isimlerini doğru şekilde kullan
        print(f"Categories found ({strategy}): {categories.keys()}")
        
        # Kategori adlarını doğru şekilde kullan
        performance = categories.get('performance', {}).get('score', 0) * 100
        accessibility = categories.get('accessibility', {}).get('score', 0) * 100
        
        # `best-practices` kategori adında tire var, Python sözlüğünde bu şekilde kullanılır
        best_practices = categories.get('best-practices', {}).get('score', 0) * 100
        seo = categories.get('seo', {}).get('score', 0) * 100
        
        # Hata ayıklama için puanları yazdır
        print(f"Scores for {url} ({strategy}): Performance={performance}, Accessibility={accessibility}, Best Practices={best_practices}, SEO={seo}")
        
        return jsonify({
            "url": url,
            "strategy": strategy,
            "performance": round(performance),
            "accessibility": round(accessibility),
            "best_practices": round(best_practices),
            "seo": round(seo)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)