from app.utils.user_validator import user_validator, generate_token

def login_service(data):
    try:
        user = user_validator(data["email"], data["password"])
        if not user:
            return {"error":"Invalid user or password!"}
        
        user_id = user["user_id"]
        token = generate_token(user_id)

        return {"token":token, "message":"Login Successfull"}
    except Exception as e:
        print("Login Error", str(e))
        return {"error":str(e)}