from os.path import join, dirname
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)