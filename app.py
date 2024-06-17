from flask import Flask, request, jsonify, send_file, render_template
import sqlite3
import qrcode
from io import BytesIO

app = Flask(__name__)

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY, data TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    event_id = request.json.get('event_id')
    data = f"http://localhost:5000/checkin?event_id={event_id}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, 'PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png', as_attachment=False, download_name='qr_code.png')

@app.route('/checkin', methods=['GET'])
def checkin():
    event_id = request.args.get('event_id')
    if not event_id:
        return jsonify({'status': 'error', 'message': 'Event ID is missing'}), 400

    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('INSERT INTO attendance (data) VALUES (?)', (event_id,))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': 'Checked in successfully'}), 200

@app.route('/attendance', methods=['GET'])
def attendance():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT data FROM attendance')
    data = c.fetchall()
    conn.close()
    return jsonify([item[0] for item in data])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)

