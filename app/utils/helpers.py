from flask import request
import json
import re
import random
from app.utils.supabase_client import supabase
from flask import request, json
import stripe

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
    if user_info:
        return json.loads(user_info)[variableName]

    return None


def stripeProductCreate(name, description, price):
    product = stripe.Product.create(
        name=name,
        description=description,
    )
    # print("Product created:", product.id)
    original_price = int(price) * 100

    price = stripe.Price.create(
        product=product.id,
        unit_amount=original_price,
        currency="inr",
    )
    # print("One-time price created:", price.id)

    return {"product": product.id, "price": price.id}


def stripeProductPriceID(name):
    products = stripe.Product.list(limit=10, expand=["data.default_price"])

    for p in products.data:
        if p.name == name:
            # print(f"\nProduct: {p.name}")

            if p.default_price:  # agar default price set hai
                amount = p.default_price["unit_amount"] / 100
                currency = p.default_price["currency"].upper()
                # print(f"  Default Price: {amount} {currency}")
            else:
                # product ke saare prices fetch karo
                prices = stripe.Price.list(product=p.id)
                if prices.data:
                    for price in prices.data:
                        amount = price.unit_amount / 100
                        currency = price.currency.upper()
                        # print(f"  Price ID: {price.id} → {amount} {currency}")
                        return price.id
                else:
                    print("  No price set for this product")