from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# Fungsi untuk koneksi ke database
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='coklat',
        cursorclass=pymysql.cursors.DictCursor
    )

# Route utama untuk menampilkan halaman HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk mengambil data coklat
@app.route('/data', methods=['GET'])
def get_data():
    score = request.args.get('score', type=float)  # Mengambil parameter score sebagai float
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            if score is not None:  # Memeriksa apakah parameter score ada
                cursor.execute("SELECT * FROM coklat WHERE skor = %s", (score,))
            else:
                cursor.execute("SELECT * FROM coklat")  # Ambil semua data jika tidak ada filter skor
            data = cursor.fetchall()
    finally:
        connection.close()

    # Iterasi untuk menampilkan data
    result = []
    for item in data:
        result.append({
            'id': item['id'],
            'nama': item['nama'],
            'asal': item['asal'],
            'cocoa_percent': item['cocoa_percent'],
            'tahun_produksi': item['tahun_produksi'],
            'rating': item['rating'],
            'negara': item['negara'],
            'skor': item['skor']
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/data', methods=['GET'])
# Fungsi rekursif untuk mengambil data berdasarkan skor
def get_data_recursive(data, index=0, result=None):
    if result is None:
        result = []

    # Jika index sudah mencapai panjang data, hentikan
    if index == len(data):
        return result

    item = data[index]
    result.append({
        'id': item['id'],
        'nama': item['nama'],
        'asal': item['asal'],
        'cocoa_percent': item['cocoa_percent'],
        'tahun_produksi': item['tahun_produksi'],
        'rating': item['rating'],
        'negara': item['negara'],
        'skor': item['skor']
    })

    # Panggil fungsi rekursif untuk item berikutnya
    return get_data_recursive(data, index + 1, result)

@app.route('/data', methods=['GET'])
def get_data():
    score = request.args.get('score', type=float)
    method = request.args.get('method', default='iterative')  # Default ke iteratif
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM coklat")
            data = cursor.fetchall()
    finally:
        connection.close()

    if method == 'iterative':
        result, _ = search_iterative(data, score)
    elif method == 'recursive':
        result, _ = search_recursive(data, score)
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify(result)

@app.route('/data', methods=['GET'])
def get_data():
    score = request.args.get('score', type=float)  # Ambil parameter score, jika ada
    method = request.args.get('method', default='iterative')  # Metode pencarian default
    connection = get_db_connection()
    
    try:
        with connection.cursor() as cursor:
            if score is not None:  # Jika ada parameter score, filter berdasarkan skor
                cursor.execute("SELECT * FROM coklat WHERE skor = %s", (score,))
            else:  # Jika tidak ada score, ambil semua data
                cursor.execute("SELECT * FROM coklat")
            data = cursor.fetchall()
    finally:
        connection.close()

    if method == 'iterative':
        result = search_iterative(data, score)
    elif method == 'recursive':
        result = search_recursive(data, score)
    else:
        return jsonify({'error': 'Invalid method'}), 400

    return jsonify(result)



#copy semua line untuk mencari iteratif dan rekrusof di chatpgt sama copy index buat nampilin dua algoritma
