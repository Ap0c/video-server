# Video Server

Flask application to serve video files on a local network, targeting the Raspberry Pi specifically. It provides a web interface for navigating content and uses Nginx to serve static files.

# Simple Install

The project comes bundled with an installation script for the Raspberry Pi. Simply download the repository, navigate to the directory, and run:

```
sudo ./setup.sh
```

Then navigate to `localhost:8080` in your browser if you are on the Pi, or `<raspberry_pi_ip_address>:8080` in your browser if you are on another computer on the network. To get the Pi's IP address, use the command:

```
hostname -I
```

# Manual Install

If, for whatever reason, the setup script does not work, or you simply want to install the project manually, the procedure is as follows.

First make sure you have Python 3 and a corresponding version of pip. Then grab a copy of the repository and set up a virtual environment called `video-server-env`, and run:

```
pip install -r requirements.txt
```

to get the dependencies. Then simply run:

```
python main.py
```

to launch the app.

## Install Nginx

The app itself is not set up to serve the media content, as this is an inefficient thing to do from Python. Instead, it is designed to run behind Nginx, which handles all requests for media, and passes requests for anything else on to the app. The following instructions for getting Nginx up and running are tailored to the Raspberry Pi (running Raspbian, a derivative of Debian), but should be easy to tweak for other systems.

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

## Configure systemd

This distribution also bundles a systemd file that allows the server to launch at boot. Again, by default it's configured to work when the repository is cloned into the home directory, so if this is not the case open up `video-server.service` and change the following lines to point to the correct location:

```
WorkingDirectory=/home/pi/video-server
Environment="PATH=/home/pi/video-server/video-server-env/bin"
ExecStart=/home/pi/video-server/video-server-env/bin/python run.py
```

Note also that this assumes a virtual environment called `video-server-env`, so if you named yours something different make sure to change this too.

Next copy this file into the `/etc/systemd/system` directory and activate using:

```
sudo systemctl enable /etc/systemd/system/video-server.service
sudo systemctl start video-server.service
```

The service should now start at boot.
