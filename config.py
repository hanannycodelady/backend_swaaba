import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:@localhost/swaaba_aralee"
    JWT_SECRET_KEY = "cars"
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploaded_images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit upload size to 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    

    

