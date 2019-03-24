virtualenv venv
pip install -r requirements.txt
source venv/bin/activate
sudo rm -rf feature_request/migrations
python manage.py setup_app