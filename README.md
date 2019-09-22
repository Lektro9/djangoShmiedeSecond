I use this for creating my website with jenkins.

# How to install
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 mysite/manage.py runserver

if you do not have a database you can create one like this:

python3 manage.py syncdb

create a superuser and you should be good to go

Otherwise message me.
