# Run this command using the source prefix "source ./setupVenv.sh"

# Creating and Activating a Python Virtual Environment to ensure that the local packages do not mess with the global packages, and also to enable better system management
red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'
# (Linux) Install VENV(Virtual ENVironment) module and PIP(Python Package Manager)
sudo apt update
printf "${yel}Updated apt packages\n${end}"
sudo apt install -y python3-venv
printf "${yel}Installed/updated VENV\n${end}"
sudo apt install -y python3-pip
printf "${yel}Installed/updated PIP\n${end}"
sudo apt install -y nginx
printf "${yel}Installed/updated Nginx\n${end}"

# Create a new virtual environment
OLDPWD=$PWD
# 1. Create a new folder in your home directory
mkdir -p ~/python-venvs
printf "${yel}Created python-venvs directory in home\n${end}"
cd ~/python-venvs
printf "${yel}Changed working directory to ~/python-venvs to \n${end}"

#2. Create a virtual environment for this project
python3 -m venv masked_calling_venv
printf "${yel}Created a new virtual environment for this project\n${end}"
#3. Enable the virtual environment
source masked_calling_venv/bin/activate
printf "${yel}Activated the virtual environment\n${end}"
cd $OLDPWD

#4. Check if the requirements.txt exist
FILE=requirements.txt
if [ -f "$FILE" ]; then
    printf "${mag}$FILE exists.\n${end}"
else
    printf "${mag}$FILE does not exist.\n${end}"
    exit 1
fi

#5. Install the requirements stored in requirements.txt
python -m pip install -r ./requirements.txt
printf "${yel}Installed/Updated required packages\n${end}"
