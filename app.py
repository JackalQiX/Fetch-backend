import json
import re
import math
import uuid
from flask import Flask, request, abort, redirect, jsonify, Response

app = Flask(__name__)
memo = {}


@app.route('/')
def index():
    return "Fetch Backend Take Home Exercise!"


@app.route('/receipts/process', methods=["POST"])
def process_receipts():
    """
    Process Receipts

    This route processes incoming receipt data, calculates points, and returns a receipt ID.

    Returns:
        dict: A JSON response with a receipt ID.
    """
    try:
        data = json.loads(request.data)
        retailer = data["retailer"]
        purchase_date = data["purchaseDate"]
        purchase_time = data["purchaseTime"]
        items = data["items"]
        total = data["total"]
        points = calculate_points(retailer, purchase_date, purchase_time, items, total)
        receipt_id = str(uuid.uuid4())
        memo[receipt_id] = points
        result = {"id": receipt_id}
        return jsonify(result)
    except KeyError:
        return abort(400, 'The receipt is invalid')


def calculate_points(retailer, purchase_date, purchase_time, items, total):
    """
    Calculate Points

    This function calculates the number of points awarded for a receipt based on specific rules.

    Args:
        retailer (str): The name of the retailer.
        purchase_date (str): The purchase date in the format 'YYYY-MM-DD'.
        purchase_time (str): The purchase time in the format 'HH:mm'.
        items (list): A list of items in the receipt:
            - "shortDescription" (str): A brief description of the item.
            - "price" (str): The price of the item as a string.
        total (str): The total amount of the receipt.

    Returns:
        int: The number of points awarded for the receipt based on the provided parameters.
    """
    date_pattern = r'^\d{4}-\d{2}-(\d{2})$'
    time_pattern = r'^(\d{2}):(\d{2})$'
    points = 0

    # One point for every alphanumeric character in the retailer name.
    for char in retailer:
        if char.isalnum():
            points += 1

    total_int = 0
    for num in total:
        if num.isnumeric():
            total_int *= 10
            total_int += int(num)

    # 50 points if the total is a round dollar amount with no cents.
    if total_int % 100 == 0:
        points += 50

    # 25 points if the total is a multiple of 0.25.
    if total_int % 25 == 0:
        points += 25

    # 5 points for every two items on the receipt.
    if items:
        points += (len(items) // 2) * 5

    # If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in items:
        try:
            short_description = item.get("shortDescription", "").strip()
            print(item, len(short_description) % 3)
            if len(short_description) % 3 == 0:
                price = float(item.get("price", 0.00))
                points += math.ceil(price * 0.2)
                print("Print!", price)
        except (ValueError, TypeError):
            pass

    # 6 points if the day in the purchase date is odd.
    day = re.search(date_pattern, purchase_date)
    if day and int(day.group(1)) % 2 == 1:
        points += 6

    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    time = re.search(time_pattern, purchase_time)
    if time and (13 < int(time.group(1)) < 16 or (time.group(1) == "16" and time.group(2) == "00")):
        points += 10
    return points


@app.route('/receipts/<id>/points')
def get_points(id):
    """
    Get Points

    This route retrieves the number of points awarded for a specific receipt by its ID.

    Args:
        id (str): The unique ID of the receipt.

    Returns:
        dict: A JSON response containing the number of points awarded.
    """
    try:
        print(memo, id)
        data = {
            "points": memo[id]
        }
        return jsonify(data)
    except KeyError:
        abort(404, 'No receipt found for that id')


if __name__ == "__main__":
    app.run()
