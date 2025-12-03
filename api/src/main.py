from flask import Flask, jsonify, request
from middleware import check_permission

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "service": "novaagro-api"})

@app.route('/harvest/<batch_id>')
def get_harvest(batch_id):
    # 1. Extract Token
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    # 2. Verify with Core Auth (via gRPC)
    if not check_permission(token):
        return jsonify({"error": "Unauthorized"}), 401

    # 3. Return Data
    return jsonify({
        "batch_id": batch_id,
        "crop": "Wheat",
        "quantity": 5000
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)