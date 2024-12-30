import os
from dotenv import load_dotenv

load_dotenv('../.settings')

port = os.getenv('LLAMAFILE_PORT')

server_url = 'http://localhost:'+port
persist_dir = './storage'
input_dir_path = '../data/texts'
request_timeout = 90
