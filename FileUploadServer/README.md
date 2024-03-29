# File Upload Server

A simple server based on the [Flask](https://flask.palletsprojects.com/en/1.1.x/) framework to upload and download files.




## Requirements

* [Flask](https://pypi.org/project/Flask/)
* [Flask-HTTPAuth](https://pypi.org/project/Flask-HTTPAuth/)
* [Pandas](https://pypi.org/project/pandas/)
* [Nginx](https://www.nginx.com/)

## How it works

A machine learning algorithm is running on the machine. As soon as there is a `.wav` file in the `input/` directory, the algorithm reads it and starts to extract features. The result of the processed file will be stored as a `.txt` file in the `output/` directory.


Using this server, audio recordings can be uploaded into the `input/` directory. As soon as the upload has finished, the client will be redirected to an URL which indicates that the file is being processed. After the algorithm has processed the file, the results will be shown as a table on this URL.
Below the table, there is a link to download the original result.

The URL's are structured as follows
(where `recording_name` is the name of the uploaded file):

URL|Description
-|-
`/`|Upload files
`/results/recording_name.wav`|After processing, the result will be shown here.
`/download/recording_name.BirdNET.selections.txt`|Download the result as `.txt` file

## Run it as a systemd service

```sh
sudo systemctl daemon-reload
sudo systemctl enable webserver.service
sudo systemctl start webserver.service
```
## HTTPS with Let's Encrypt and Nginx

According to [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04)


