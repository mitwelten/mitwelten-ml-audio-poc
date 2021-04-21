#!usr/bin/python3

# License:
# https://fhnw.mit-license.org/

import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template, send_file
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd

from credentials import password

# Files are uploaded to the input/ folder
UPLOAD_FOLDER = 'input'

# Files can be downloaded from the output/ folder
RESULT_FOLDER='output'

# only accept .wav files
ALLOWED_EXTENSIONS = {'wav'}

user_pw = password()

# one user
# https://flask-httpauth.readthedocs.io/en/latest/
users = {
    "mitwelten": generate_password_hash(str(user_pw))
}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(SECRET_KEY=os.urandom(12))

auth = HTTPBasicAuth()

# Display a banner indicating a warning
def getWarning(warning=None):
    if(warning):
        
        warn = """
                <style>
        .alert {
            margin-top:20px;
        padding: 20px;
        background-color: #f44336;
        color: white;
        }

        .closebtn {
        margin-left: 15px;
        color: white;
        font-weight: bold;
        float: right;
        font-size: 22px;
        line-height: 20px;
        cursor: pointer;
        transition: 0.3s;
        }

        .closebtn:hover {
        color: black;
        }
        </style>
        <div class="alert">
        <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>"""+warning+"""
        </div>
        """
        return warn
    return ""


# check if the filetype is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# get the filename without extension
def getNameWoExtension(filename):
    return filename.rsplit('.', 1)[0]

# convert a tab-seperated file to a html table
def showTable(filename):
    newfilename=getNameWoExtension(filename)+".BirdNET.selections.txt"
    fullname=(RESULT_FOLDER+"/"+newfilename)
    try:
        a = pd.read_csv(fullname,sep='\t')
        # sort by time and rank
        a.sort_values(["Begin Time (s)","Rank"],inplace=True)
        # drop columns View, Channel, Frequencyes and Filename
        a.drop(columns="View",inplace=True)
        a.drop(columns="Channel",inplace=True)
        a.drop(columns="Low Freq (Hz)",inplace=True)
        a.drop(columns="High Freq (Hz)",inplace=True)
        a.drop(columns="Begin File",inplace=True)
        return a.to_html(index=False)+"""<p> <a href="/download/"""+filename+""""/>Download</a></p>"""
    except:
        return "Could not display the results"

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

# Route for results
@app.route('/uploads/<filename>')
@auth.login_required
def uploaded_file(filename):
    #filename without extension + BirdNET.selections.txt
    newfilename=getNameWoExtension(filename)+".BirdNET.selections.txt"
    fullname=(RESULT_FOLDER+"/"+newfilename)
    
    if not os.path.isfile(fullname):
        return """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width">
                <title>Your record is being processed</title>
            <meta http-equiv="refresh" content="5">
            </head>
            <body>
                <h1>"""+getNameWoExtension(filename)+""" is being processed.
                
                </h1>
                <h3>
                The result will be shown here.
                </h3>
            </body>
        </html>
        """
    return showTable(filename)



# download the original result 
@app.route('/download/<filename>')
@auth.login_required
def downloadFile (filename):
    newfilename=getNameWoExtension(filename)+".BirdNET.selections.txt"
    print(newfilename)
    path = (RESULT_FOLDER+"/"+newfilename)
    if not os.path.isfile(path):
        return """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width">
                <title>Your record is being processed</title>
            <meta http-equiv="refresh" content="5">
            </head>
            <body>
                <h1>"""+getNameWoExtension(filename)+""" is being processed.
                
                </h1>
                <h3>
                The result will be shown here.
                </h3>
            </body>
        </html>
        """
    
    return send_file(path, as_attachment=True)


# route for uploading files
@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def upload_file():
    warning=None
    if request.method == 'GET':
        return '''
            <!doctype html>
            <html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            ''' + getWarning(warning)
    else if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            warning="No file found"
            return redirect(request.url)
        file = request.files['file']
        if not file: # or file == None
            warning="No file found"
        else:
            if file.filename == '':
                warning="No file found"
            else: # filename != ''
                if not allowed_file(file.filename):
                    warning="Format not supported. Try a <strong>.wav</strong> file"
                else: # allowed_file
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    #https://stackoverflow.com/questions/14810795/flask-url-for-generating-http-url-instead-of-https/37842465#37842465
                    return redirect(url_for('uploaded_file',
                                                filename=filename,_external=True,_scheme="https"))
    else:
        abort(405, 'Method Not Allowed')

# run the server
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0') # using default port 5000
    
