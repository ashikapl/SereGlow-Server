import jwt
from functools import wraps
from flask import request, jsonify, redirect, url_for
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SUPABASE_APIKEY")


# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth_header = request.headers.get("Authorization")
#         print(auth_header)
#         if not auth_header:
#             return jsonify({"error": "Token Missing!"}), 401
#         try:
#             token = auth_header.split(" ")[1]
#             data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             user_id = data["user_id"]
#         except jwt.ExpiredSignatureError:
#             return jsonify({"error": "Token Expired!"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"error": "Invalid User!"}), 401
#         return f(user_id=user_id, *args, **kwargs)
#     return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("AdminToken")
        # print(token)
        # if not token:
        #     abort(403)
        if not token:
            # No token → login page
            return redirect(url_for("admin_bp.show_admin_login"))

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            admin_id = data["admin_id"]
        except jwt.ExpiredSignatureError:
            # Expired → login page
            return redirect(url_for("admin_bp.admin_login"))
        except jwt.InvalidTokenError:
            # Invalid → login page
            return redirect(url_for("admin_bp.admin_login"))

        return f(*args, **kwargs)
    return decorated

def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("UserToken")
        # print(token)
        # if not token:
        #     abort(403)
        if not token:
            # No token → login page
            return redirect(url_for("user_bp.show_user_login"))

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            # Expired → login page
            return redirect(url_for("user_bp.user_login"))
        except jwt.InvalidTokenError:
            # Invalid → login page
            return redirect(url_for("user_bp.user_login"))

        return f(*args, **kwargs)
    return decorated


