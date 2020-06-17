Steps to run the project
1) Unzip the downloaded file
2) go to the directory
3) Install pip first

sudo apt-get install python3-pip

4)Then install virtualenv using pip3

sudo pip3 install virtualenv 

5)Now create a virtual environment

virtualenv venv 

Few Tips :
you can use any name insted of venv

You can also use a Python interpreter of your choice

virtualenv -p /usr/bin/python2.7 venv

6)Active your virtual environment:

Using Linux:

source venv/bin/activate 
(Where venv is the name of you virtual env)

Using fish shell:

source venv/bin/activate.fish

To deactivate:

deactivate

7) Install the requirements using
pip install -r requirements.txt

If you are using python3 then you have to use pip3 install -r requirements.txt

8) run python manage.py makemigrations

9) Run python manage.py migrate

10) Run python manage.py runserver 

this will start the server on localhost at 8000 port 

to change the port simply add the port number after runserver eg: python manage.py runserver 8080 to run the server on port 8080

11)To create super user run python manage.py createsuperuser
follow the instructions and your super user will be created this is your admin user




Additional information for python 3:
1)Create virtualenv using Python3

virtualenv -p python3 myenv

Instead of using virtualenv you can use this command in Python3

python3 -m venv myenv



