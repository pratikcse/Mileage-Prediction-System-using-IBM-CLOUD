import requests
import csv
from datetime import datetime

API_KEY = "tfDOSvhF2udsnjCgKsYAlyxAiGUrcoY16d3vfh1n9Lz0"
TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"
SCORING_URL = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2ffbc595-41a6-41b5-916a-31aef4ee87b7/predictions?version=2021-05-01"

headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": API_KEY
}

token_response = requests.post(TOKEN_URL, headers=headers, data=data)
mltoken = token_response.json().get("access_token")
if not mltoken:
    print("❌ Token Error:", token_response.text)
    exit()

header_csv = ["Date & Time", "Cylinders", "Displacement", "Horsepower", "Weight", "Acceleration", "Model Year", "Origin", "Car Name", "Prediction"]

try:
    with open("predictions.csv", "x", newline="") as file:
        csv.writer(file).writerow(header_csv)
except FileExistsError:
    pass

print("\n🔁 Car Prediction System Started\n")

while True:
    try:
        cylinders = int(input("Enter number of cylinders: "))
        displacement = float(input("Enter engine displacement: "))
        horsepower = float(input("Enter horsepower: "))
        weight = float(input("Enter weight: "))
        acceleration = float(input("Enter acceleration: "))
        model_year = int(input("Enter model year: "))
        origin = int(input("Enter origin (1=USA, 2=Europe, 3=Asia): "))
        car_name = input("Enter car name: ")

        payload = {
            "input_data": [
                {
                    "fields": ["cylinders", "displacement", "horsepower", "weight", "acceleration", "model year", "origin", "car name"],
                    "values": [[cylinders, displacement, horsepower, weight, acceleration, model_year, origin, car_name]]
                }
            ]
        }

        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {mltoken}'}
        response = requests.post(SCORING_URL, json=payload, headers=headers)
        result = response.json()

        # Check if prediction exists
        if "predictions" not in result:
            print("❌ Prediction Error:", result)
            break

        prediction = result["predictions"][0]["values"][0][0]
        print(f"\n✅ Predicted MPG (Mileage): {prediction}\n")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("predictions.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([now, cylinders, displacement, horsepower, weight, acceleration, model_year, origin, car_name, prediction])

        again = input("Do you want to predict again? (y/n): ").lower()
        if again != "y":
            print("\n✅ Thank you for using the system. CSV file saved as predictions.csv ✅")
            break

    except Exception as e:
        print("❌ Error:", e)
        break
