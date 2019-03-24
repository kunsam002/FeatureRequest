virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
sudo rm -rf feature_request/migrations
python manage.py setup_app