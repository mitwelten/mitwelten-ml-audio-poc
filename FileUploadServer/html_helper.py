import pandas as pd


def get_upload_form(warning=None):
    upload_form = """
        <!doctype html>
        <html>
        <head>
        <title>Upload new File</title>
        <link rel="icon"  href="/favicon.png">
        </head>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>"""
    if not warning:
        return upload_form
    else:
        return (
            upload_form
            + """
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
            <span class="closebtn" onclick="this.parentElement.style.display='none';">&times;</span>"""
            + warning
            + """
            </div>
            """
        )


def is_being_processed(filename):
    return (
        """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width">
                <title>Your record is being processed</title>
                <link rel="icon"  href="/favicon.png">
            <meta http-equiv="refresh" content="5">
            </head>
            <body>
                <h1>"""
        + str(filename)
        + """ is being processed.
                </h1>
                <h3>
                The result will be shown here.
                </h3>
            </body>
        </html>
        """
    )


def get_result_table(file_path):
    html_head = """
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width">
                <title>Result</title>
                <link rel="icon"  href="/favicon.png">
            </head>
            <style>
                table{
                width: 100%;
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                }
                th{
                background-color: #4CAF50;
                padding: 8px;
                }
                td{
                padding: 4px;
                }
            </style>"""

    try:
        df = pd.read_csv(file_path, sep="\t")  # Read the file
        df.sort_values(
            ["Begin Time (s)", "Rank"], inplace=True
        )  # sort by time and rank
        df.drop(columns="View", inplace=True)  # Drop column View
        df.drop(columns="Channel", inplace=True)  # Drop column Channel
        df.drop(columns="Low Freq (Hz)", inplace=True)  # Drop column Low Freq
        df.drop(columns="High Freq (Hz)", inplace=True)  # Drop column High Freq
        df.drop(columns="Begin File", inplace=True)  # Drop column Begin File
        return html_head + df.to_html(index=False)
    except:
        return "No preview available"


def get_download_link(filename):
    return """<p> <a href="/download/""" + filename + """"/>Download as txt file</a></p>"""

def get_result_json(file_path):
    try:
        df = pd.read_csv(file_path, sep="\t")  # Read the file
        df.sort_values(
            ["Begin Time (s)", "Rank"], inplace=True
        )  # sort by time and rank
        return  df.to_json(index=False)
    except:
        return '{"parsingError":"true"}'