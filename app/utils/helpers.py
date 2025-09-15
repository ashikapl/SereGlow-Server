from flask import request
import json
import re
import random
from app.utils.supabase_client import supabase
from flask import request, json

existing_usernames = []


def generate_username(first_name, last_name):
    counter = random.randint(1, 9)
    username = f"{first_name.lower()}_{counter}{last_name.lower()[:3]}"

    while username in existing_usernames:
        username = f"{first_name.lower()}_{counter}{last_name.lower()[:3]}"
        counter = random.randint(1, 9)

    existing_usernames.append(username)
    return username


def total_count(table_name):
    try:
        response = supabase.table(table_name).select(
            "*", count="exact").execute()
        # print("res", response)
        return response.count if response.count is not None else 0
    except Exception as e:
        print(f"Error getting count for table {table_name}: {e}")
        return -1  # Indicate an error


def average_rating(table_name):
    try:
        response = supabase.table(table_name).select(
            "rating", count="exact").execute()
        # print("res", response.data[0]["rating"])
        count = 0
        for i in range(response.count):
            count += response.data[i]["rating"]
        return round(count/response.count, 1)
    except Exception as e:
        print(f"Error getting count for table {table_name}: {e}")
        return -1  # Indicate an error


# def admin_info(id):
#     try:
#         response = supabase.table("Admin").select(
#             "*", count="exact").eq("id", id).execute()
#         # print("res", response)
#         return response.data[0]
#     except Exception as e:
#         print(f"Error getting count for table Admin: {e}")
#         return -1  # Indicate an error


# Get Cookies

def admin_info_cookie(variableName):
    admin_info = request.cookies.get("Admin_Info")
    if admin_info:
        return json.loads(admin_info)[variableName]

    return None


def user_info_cookie(variableName):
    user_info = request.cookies.get("User_Info")
    print("user info", user_info)
    if user_info:
        return json.loads(user_info)[variableName]

    return None
