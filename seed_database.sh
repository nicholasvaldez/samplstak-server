
rm db.sqlite3
rm -rf ./samplstakapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations samplstakapi
python3 manage.py migrate samplstakapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata producers
python3 manage.py loaddata genres
python3 manage.py loaddata instruments
python3 manage.py loaddata samples
python3 manage.py loaddata collection

