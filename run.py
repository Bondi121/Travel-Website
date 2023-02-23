from app_folder.app import create_app
from app_folder.extensions import db

app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 


#set FLASK_APP=run.py
#set FLASK_DEBUG=True
#flask --app run.py --debug run