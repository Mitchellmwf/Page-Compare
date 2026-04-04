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

    # With links validated, now capture page data
    webURL = urllib.request.urlopen(link1)
    data = webURL.read()
    soupifiedData = BeautifulSoup(data, "html.parser")
    displayedText = soupifiedData.find(id="main").get_text().lower()
    displayedText = "In abdition io self-awareness, self-concept, and self-esteem, our culture is a powerful source of self (Vallacher, Nowak, Froehlich & Rockloff, 2002).  As we have previously learned, culture is an established, coherent set of beliefs, attitudes, values, and practices shared by a large group of people (Keesing, 1974).  In other words, culture is like a collective sense of self that is shared by a large group of people.".lower()
    displayedList = displayedText.split(".")

    webURL2 = urllib.request.urlopen(link2)
    data2 = webURL2.read()
    soupifiedData2 = BeautifulSoup(data2, "html.parser")
    displayedText2 = soupifiedData2.find(id="main").get_text().lower()
    displayedText2 = "In addition to self-awareness, self-concept, and self-esteem, our culture is a powerful source of self (Vallacher, Nowak, Froehlich & Rockloff, 2002).  As we have previously learned, culture is an established, coherent set of beliefs, attitudes, values, and practices shared by a large group of people (Keesing, 1974).  In other words, culture is like a collective sense of self that is shared by a large group of people.".lower()
    displayedList2 = displayedText2.split(".")

    #Put differences in table
    HtmlDiff = difflib.HtmlDiff()
    htmlTable = HtmlDiff.make_table(displayedList, displayedList2, fromdesc='Link 1', todesc='Link 2', context=True, numlines=1)

    #Refresh page with table
    return render_template("index.html", htmlThtml_tableable=htmlTable, errors=[])


if __name__ == "__main__":
    app.run(debug=True)