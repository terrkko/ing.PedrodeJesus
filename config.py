import os

class Config:
    SECRET_KEY = "3e1f4b768efb8d96ab2fc230f19807b390ef7e6e76cc5ec8120c3021d849b676"
    
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://pguser:Wm9%40Qs41%21Lp8%23Vk27@ep-billowing-recipe-aevtjkfl-pooler.c-2.us-east-2.aws.neon.tech:5432/passwordsdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Genera una key con:
    # >>> from cryptography.fernet import Fernet; print(Fernet.generate_key())
    FERNET_KEY = b"NCNeuMlgRk8CgX7_G7cCiEjukaxXW-n_3G2mgL_gDbA="
