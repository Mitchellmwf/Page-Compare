from flask import Flask, render_template, request, redirect, url_for, flash
from urllib.parse import urlparse
import urllib.request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.secret_key = "DFghBN$JMK!BN"  # Required for flash messages

headers = {"User-Agent": "Mozilla/5.0"}

def is_valid_url(url: str) -> bool:
    """Basic URL validation."""
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", displayedList1=[])


@app.route("/submit", methods=["POST"])
def submit():
    link1 = request.form.get("link1", "").strip()
    link2 = request.form.get("link2", "").strip()
    errors = {}
    if not link1:
        errors["link1"] = "Please paste a URL."
    elif not is_valid_url(link1):
        errors["link1"] = "Must be a valid URL (include https://)."

    if not link2:
        errors["link2"] = "Please paste a URL."
    elif not is_valid_url(link2):
        errors["link2"] = "Must be a valid URL (include https://)."

    if errors:
        return render_template(
            "index.html",
            errors=errors,
            form_data={"link1": link1, "link2": link2},
            displayedList1=[]
        )

    # ── Do something with the links here ──────────────────────────────────────
    #capture webpage data as a list
    webURL = urllib.request.urlopen(link1)
    data = webURL.read()
    soupifiedData = BeautifulSoup(data, "html.parser")
    displayedText = soupifiedData.get_text().lower()
    displayedList2 = displayedText.split()
    #capture webpage data as a list using requests
    response = requests.get(link2, headers=headers)
    soupifiedData = BeautifulSoup(response.text, "html.parser")
    displayedText = soupifiedData.get_text().lower()
    displayedList1 = displayedText.split()
    # ──────────────────────────────────────────────────────────────────────────

    return render_template("index.html", displayedList1=displayedList1, errors=[])


if __name__ == "__main__":
    app.run(debug=True)