#!usr/bin/python3

# License:
# https://fhnw.mit-license.org/

import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
    render_template,
    send_file,
    abort,
)
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from credentials import password
from html_helper import (
    get_upload_form,
    get_result_table,
    is_being_processed,
    get_download_link,
)


UPLOAD_FOLDER = "/home/ubuntu/BirdNET/input"  # The directory to upload to


RESULT_FOLDER = "/home/ubuntu/BirdNET/output"  # The directory to download files from

ALLOWED_EXTENSIONS = {"wav"}  # File extensions that are allowed

user_pw = password()  # get password from credentials.py


# https://flask-httpauth.readthedocs.io/en/latest/
users = {"mitwelten": generate_password_hash(str(user_pw))}

app = Flask(__name__)
auth = HTTPBasicAuth()

# Check if filetype is allowed
def file_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_result_filename(filename):
    return filename.rsplit(".", 1)[0] + ".BirdNET.selections.txt"


def file_exists(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route("/favicon.ico", methods=["GET"])
@auth.login_required
def favicon():
    return send_file("favicon.ico")


# route for uploading files
@app.route("/", methods=["GET", "POST"])
@auth.login_required
def upload_file():
    if request.method == "GET":
        return get_upload_form()
    else:
        if request.method == "POST":
            # check if the post request has the file part
            if "file" not in request.files:
                return get_upload_form("No file found"),400
            file = request.files["file"]
            if not file:  # or file == None
                return get_upload_form("No file found"),400
            else:
                if file.filename == "":
                    return get_upload_form("No file found")
                else:  # filename != ''
                    if not file_allowed(file.filename):
                        return get_upload_form(
                            "Format not supported. Try a <strong>.wav</strong> file"
                        ),400
                    else:  # allowed_file
                        filename = secure_filename(file.filename)
                        if file_exists(
                            RESULT_FOLDER + "/" + get_result_filename(filename)
                        ):
                            return get_upload_form(
                                """A file with the name  <a href="/result/"""
                                + filename
                                + """"/>"""
                                + filename
                                + """</a> already exists. Please rename it."""
                            ),400
                        else:
                            file.save(os.path.join(UPLOAD_FOLDER, filename))
                            # https://stackoverflow.com/questions/14810795/flask-url-for-generating-http-url-instead-of-https/37842465#37842465
                            return redirect(
                                url_for(
                                    "show_output",
                                    filename=filename,
                                    _external=True,
                                    _scheme="https",
                                )
                            )
        else:
            return abort(405, "Method Not Allowed")


@app.route("/result/<filename>", methods=["GET"])
@auth.login_required
def show_output(filename):
    filename = secure_filename(filename)
    result_filename = get_result_filename(filename)
    result_file_path = RESULT_FOLDER + "/" + result_filename
    if os.path.isfile(result_file_path):
        return get_result_table(result_file_path) + get_download_link(result_filename)
    else:
        return is_being_processed(filename)


# download the original result
@app.route("/download/<filename>", methods=["GET"])
@auth.login_required
def download_file(filename):
    filename = secure_filename(filename)
    result_file_path = RESULT_FOLDER + "/" + filename
    if os.path.isfile(result_file_path):
        return send_file(result_file_path, as_attachment=True)
    else:
        return is_being_processed(filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
