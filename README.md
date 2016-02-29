# Video Server

Flask application to serve video files on a local network.

# Install

First make sure you have Python 3 and a corresponding version of pip. Then grab a copy of the repository and do:

```
pip install -r requirements.txt
```

to get the dependencies. Then simply run:

```
python main.py
```

to launch the app.

# Media

The app itself is not set up to serve the media content, as this is an inefficient thing to do from Python. Instead, it is designed to run behind Nginx, which handles all requests for media, and passes requests for anything else on to the app. The following instructions for getting Nginx up and running are tailored to the Raspberry Pi (running Raspbian, a derivative of Debian), but should be easy to tweak for other systems.

## Install Nginx

First, to install Nginx:

```
sudo apt-get install nginx
```

## Configure Nginx

Then open up the config file `/etc/nginx/nginx.conf` and add `disable_symlinks off;` to the http section, so that it looks something like this:

```
http {
    disable_symlinks off;

    ...
}

```

Now it's time to let Nginx know about the video server. Bundled with this repository is a file called `nginx-config`, open it up and find the following section:

```
location /media/ {
    alias /home/pi/video-server/media/;
}
```

This path assumes the video server has been cloned into the Raspberry Pi home directory. If it has been placed somewhere else, change the alias path to point to this location instead (make sure that it points to the `media` subdirectory within the repository).

Now copy this file into the Nginx `sites-available` directory:

```
sudo cp nginx-config /etc/nginx/sites-available/video-server
```

and link it into the `sites-enabled` directory:

```
sudo ln -s /etc/nginx/sites-available/video-server /etc/nginx/sites-enabled/video-server
```

Finally, reload the Nginx config with:

```
sudo nginx -s reload
```

Nginx should now be up and running, and serving the contents of the `media` directory.
