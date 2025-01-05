from flask import Flask, request, jsonify, url_for
from itsdangerous import URLSafeTimedSerializer
import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
serializer = URLSafeTimedSerializer(app.secret_key)

# Generate token
def generate_reset_token(email):
    return serializer.dumps(email, salt='password-reset-salt')

# Verify token
def verify_reset_token(token, expiration=900):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
        return email
    except Exception:
        return None

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.json['email']
    token = generate_reset_token(email)
    reset_url = url_for('reset_password', token=token, _external=True)
    return jsonify({"message": "Password reset link sent", "reset_url": reset_url})

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if email is None:
        return jsonify({"message": "Invalid or expired token"}), 400
    new_password = request.json['new_password']
    # Update password in database (hashing included)
    return jsonify({"message": "Password updated successfully"})

if __name__ == '__main__':
    app.run(debug=True)
