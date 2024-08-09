import pandas as pd
from cryptography.fernet import Fernet
import os


def encrypt(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt(data):
    return cipher.decrypt(data.encode()).decode()

def save_file(file, save_path):
    with open(save_path, 'wb') as f:
        f.write(file.read())

def process_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
       
        pass
    elif ext == '.docx':
      
        pass
    elif ext == '.txt':
      
        with open(file_path, 'r') as file:
            return file.read()
    return ""
