from flask import Flask, render_template, request, redirect
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Load credentials from environment variable
creds_json = os.environ.get("GOOGLE_CREDS_JSON")

if not creds_json:
    raise ValueError("Environment variable GOOGLE_CREDS_JSON not set")

creds_dict = json.loads(creds_json)


scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("Demo_reg").sheet1


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    class_name = request.form["class"]
    roll = request.form["roll"]
    num1 = request.form["num1"]
    num2 = request.form["num2"]

    # Append data as new row
    sheet.append_row([name, class_name, roll, num1, num2])

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False)
