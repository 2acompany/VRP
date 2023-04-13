# VRPModel Setup 

# install Python and set virtual environment https://www.python.org/downloads/

setup virtual environment for first time 
#python -m venv env
#env\Scripts\activate.bat
create requirements after installing all packages 
#pip freeze > requirements.txt - To create the file, run this

with virtual environment
#pip --timeout=1000 install -r requirements.txt- This will install all the packages listed in #the requirements.txt file and their dependencies.

incase you are using global dependencies 
#env\Scripts\deactivate.bat - This command will deactivate the virtual environment and restore your system's original PATH
#pip --timeout=1000 install -r requirements.txt- This will install all the packages listed in #the requirements.txt file and their dependencies.


without virtual environment
#pip install Flask, ...... and all other dependencies listed on requirements.txt

#some tips 
py -m pip --timeout=1000 install -U scikit-learn 

# install git from https://git-scm.com/downloads

#git config --global user.name "w3schools-test"
#git config --global user.email "test@w3schools.com"
#git clone https://github.com/behrangaghili/VRP

# if you are a collaborator

#git pull
#git rm -rf --cached .
#git rm -r --cached __pycache__/
#git add .
#git commit -m "name of commit "
#git push

# Make This Repo a Service in Windows
call nssm.exe install VRPApplicationPython "%cd%\VRPApplicationPython.bat"
call nssm.exe set VRPApplicationPython AppStdout "%cd%\logs\VRPApplicationPython_logs.log"
call nssm.exe set VRPApplicationPython AppStderr "%cd%\logs\VRPApplicationPython_logs.log"
call nssm set VRPApplicationPython AppRotateFiles 1
call nssm set VRPApplicationPython AppRotateOnline 1
call nssm set VRPApplicationPython AppRotateSeconds 86400
call nssm set VRPApplicationPython AppRotateBytes 1048576
call sc start VRPApplicationPython
nssm edit  VRPApplicationPython
sc query VRPApplicationPython


# Set Venv on Deployment Server
 changed the file :
.venv/pyvenv.cfg 

Inside it modify this variable
home = C:\Python39 to python dirctory 
# linux Deployment
to run your flask  app on port 5000 and listen on all available network interfaces, you can set the host parameter to 0.0.0.0 and the port parameter to 5000 like this:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
Alternatively, you can set the host and port values as environment variables so that they can be easily changed without modifying the code.
 You can access these environment variables using the os module in Python. Here's an example:
 import os
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
In this example, the os.environ.get() method is used to retrieve the values of the HOST and PORT environment variables, with default values of 0.0.0.0 and 5000 respectively. This allows you to easily change the host and port values without modifying the code.


# run app on linux and chack firewall 
Allow incoming traffic to the appropriate port: You will need to configure the firewall to allow incoming traffic to the port that your Flask app is listening on. For example, if your app is listening on port 80 for HTTP traffic, you can allow incoming traffic to that port using the following command:

sudo ufw allow 80/tcp

If you are using HTTPS (port 443), you can allow incoming traffic to that port using the following command:

sudo ufw allow 443/tcp

Configure the firewall to allow outgoing traffic: You will also need to configure the firewall to allow outgoing traffic from your server. This can be done by default on most distributions, but it's a good idea to double-check

Set up a reverse proxy: It is good practice to use a reverse proxy such as NGINX or Apache to handle incoming requests to your Flask app. The reverse proxy can also be configured to serve static files and handle other tasks such as caching and load balancing. Here's an example of how to set up a reverse proxy using NGINX:
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

in this case I used:
server {
    listen 80;
    listen [::]:80;
    server_name vrp.shipito.ir;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

Here's what this configuration does:

    The listen directive specifies that Nginx should listen on port 80 for incoming requests.
    The server_name directive specifies the hostname that this server block should apply to (vrp.shipito.ir in this case).
    The location block sets up a reverse proxy to forward incoming requests to your Flask app running on port 5000 on the same machine (http://127.0.0.1:5000).
    The proxy_set_header directives are used to pass along the original client's IP address and hostname to your Flask app.

Save this configuration file to a file in the /etc/nginx/sites-available/ directory (e.g. /etc/nginx/sites-available/vrp.shipito.ir) and then create a symbolic link to it in the /etc/nginx/sites-enabled/ directory using the following command:

sudo ln -s /etc/nginx/sites-available/vrp.shipito.ir /etc/nginx/sites-enabled/

Finally, test your Nginx configuration using the following command:

sudo nginx -t


Restart the firewall and reverse proxy: Once you have made changes to the firewall or reverse proxy configuration, you will need to restart the relevant services to apply the changes. For example, if you are using NGINX, you can restart it using the following command:

sudo systemctl restart nginx

# install ssl lets encrypt 
here are the steps to install SSL certificates from Let's Encrypt on your Nginx server:

    Install Certbot: Certbot is a tool for obtaining and renewing SSL/TLS certificates from Let's Encrypt. You can install Certbot on Ubuntu using the following commands:

sudo apt update
sudo apt install certbot python3-certbot-nginx

Obtain an SSL/TLS certificate: Once you have Certbot installed, you can use it to obtain an SSL/TLS certificate for your domain by running the following command:

sudo certbot --nginx -d vrp.shipito.ir

This command will run Certbot in "nginx" mode and automatically configure Nginx to use the SSL/TLS certificate. You will be prompted to enter an email address for notifications and to agree to the Let's Encrypt terms of service. Certbot will then verify that you control the domain and automatically obtain and install the SSL/TLS certificate.

    Test the SSL/TLS configuration: Once Certbot has obtained the SSL/TLS certificate and configured Nginx, you can test the SSL/TLS configuration using a tool like Qualys SSL Labs' SSL Server Test. This will ensure that your server is properly configured and secure.

    Set up automatic renewal: Let's Encrypt certificates are valid for 90 days, so it's important to set up automatic renewal to ensure that your SSL/TLS certificate remains valid. Certbot will automatically configure a cron job to renew the certificate when it is close to expiring. You can test the renewal process by running the following command:

sudo certbot renew --dry-run

This will simulate a renewal attempt and ensure that everything is working correctly.

That's it! With these steps, you should have a valid SSL/TLS certificate from Let's Encrypt installed on your Nginx server, providing secure HTTPS access to your Flask app through your domain vrp.shipito.ir.

to Ensure that your SSL/TLS certificate is properly installed: Verify that your SSL/TLS certificate is properly installed on your server and that it is configured to be used by your web server. You can use the following command to check the SSL/TLS configuration of your website:

sudo nginx -T | grep ssl

This will display the SSL/TLS configuration of your website. Ensure that the certificate and key files are correctly specified.

    Verify that your website is accessible over HTTPS: Ensure that your website is accessible over HTTPS by using the HTTPS protocol instead of HTTP in the URL (e.g. https://vrp.shipito.ir instead of http://vrp.shipito.ir). If your website is not accessible over HTTPS, you may need to adjust your Nginx configuration or firewall settings.

    Clear your browser cache: Sometimes SSL errors can be caused by cached SSL certificates in your browser. Try clearing your browser cache and cookies and then accessing your website again.

    Check your SSL/TLS settings: Ensure that your SSL/TLS settings are configured properly in your web server and browser. For example, ensure that your browser is set to use the most secure SSL/TLS protocol and cipher suite.