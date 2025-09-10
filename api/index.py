from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "✅ API Check Token Account đang chạy!"
    })


@app.route("/api/check_token_file", methods=["GET"])
def check_token_file():
    # 🔑 Bảo mật bằng key
    key = request.args.get("key")
    if key != "hentaiz":
        return jsonify({"error": "❌ Unauthorized. Invalid key!"}), 403

    # Lấy token(s)
    token_file = request.args.get("token_file")
    if not token_file:
        return jsonify({"error": "❌ token_file parameter is required"}), 400

    results = []
    tokens = token_file.split(",")  # hỗ trợ nhiều token cách nhau bằng dấu phẩy

    for idx, token in enumerate(tokens, start=1):
        token = token.strip()
        try:
            # Decode JWT không cần verify chữ ký
            decoded = jwt.decode(token, options={"verify_signature": False})

            # Xử lý thời gian hết hạn
            exp_ts = decoded.get("exp")
            exp_time = None
            expired = None
            message = "Không có thời gian hết hạn"

            if exp_ts:
                exp_time = datetime.datetime.fromtimestamp(exp_ts)
                now = datetime.datetime.utcnow()
                expired = exp_time < now
                message = (
                    f"Token expired at {exp_time}"
                    if expired
                    else f"Token valid until {exp_time}"
                )

            results.append({
                "index": idx,
                "status": "success",
                "message": message,
                "decode_message": "✅ Token decode thành công",
                "expired": expired,
                "exp_time": exp_time.strftime("%Y-%m-%d %H:%M:%S") if exp_time else None,
                "payload": decoded,
                "token": token  # 👈 Hiện FULL token, không rút gọn nữa
            })

        except Exception as e:
            results.append({
                "index": idx,
                "status": "error",
                "message": f"❌ Decode lỗi: {str(e)}",
                "decode_message": "❌ Token decode thất bại",
                "expired": None,
                "exp_time": None,
                "payload": None,
                "token": token
            })

    return jsonify({"results": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)
