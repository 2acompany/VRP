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



# install git from https://git-scm.com/downloads

#git config --global user.name "w3schools-test"
#git config --global user.email "test@w3schools.com"
#git clone https://github.com/behrangaghili/VRP

# if you are a collaborator

#git pull
#git rm -rf --cached .
#git add .
#git commit -m "name of commit "
#git push

#Run NSSM
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