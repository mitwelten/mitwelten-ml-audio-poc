# Nginx config

The file [webserver](webserver) is in `/etc/nginx/sites-available`

To enable, add a link to `/etc/nginx/sites-enabled`

```sh
sudo ln -s /etc/nginx/sites-available/webserver /etc/nginx/sites-enabled
```

> To allow the upload of larger files, `client_max_body_size` was set to 1000M;