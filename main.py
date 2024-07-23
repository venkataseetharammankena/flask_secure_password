import pyperclip
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from password_generator import generator

app = Flask(__name__)
app.secret_key = "SECRET_KEY"


@app.route("/")
def home():
    if "chars" not in session:
        session["chars"] = ["uppercase", "lowercase", "digits", "symbols"]
    if "len_range_value" not in session:
        session["len_range_value"] = 14
    if "secure_password" not in session:
        chars = session["chars"]
        len_range_value = session["len_range_value"]

        session["secure_password"] = generator(
            length=int(len_range_value),
            uppercase="uppercase" in chars,
            lowercase="lowercase" in chars,
            digits="digits" in chars,
            symbols="symbols" in chars,
        )

    chars = session["chars"]
    len_range_value = session["len_range_value"]
    secure_password = session["secure_password"]

    return render_template(
        "home.html",
        chars=chars,
        len_range_value=len_range_value,
        secure_password=secure_password,
    )


@app.route("/generate/", methods=["GET", "POST"])
def generate():
    if request.method == "POST":
        chars = request.form.getlist("char_box")
        len_range_value = request.form.get("len_range")
        secure_password = generator(
            length=int(len_range_value),
            uppercase="uppercase" in chars,
            lowercase="lowercase" in chars,
            digits="digits" in chars,
            punctuation="punctuation" in chars,
        )

        if len(chars) != 0:
            session["chars"] = chars
            session["len_range_value"] = len_range_value
            session["secure_password"] = secure_password
            return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/copy/")
def copy():
    secure_password = session["secure_password"]
    pyperclip.copy(secure_password)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
