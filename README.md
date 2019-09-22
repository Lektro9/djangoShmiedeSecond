I use this for creating builds of my website with jenkins.

# How to install
sudo apt-get install python3-pip <br>
sudo pip3 install virtualenv <br>
virtualenv venv <br>
source venv/bin/activate <br>
pip3 install -r requirements.txt <br>
python3 mysite/manage.py runserver <br>

if you do not have a database you can create one like this: <br>

python3 manage.py syncdb <br>

create a superuser and you should be good to go <br>

Otherwise message me.
