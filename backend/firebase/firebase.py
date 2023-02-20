import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from app.core.config import settings

cred = credentials.Certificate('find-your-place-d7479-firebase-adminsdk-mgwkv-e0b4924f1d.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': settings.FIREBASE_URL
})

ref = db.reference('/')
print(ref.get())