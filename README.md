```
git clone https://github.com/mackjoner/microwebpy.git
cd webpy
virtualenv venv
source ./venv/bin/active
pip install -r requirements.txt
python app.py
```
app deploy
```
gunicorn -b $ip:$port -w $work_num app:wsgi_app -D
```
