import os
import json
import hashlib
import requests

from dotenv import load_dotenv

load_dotenv()

FILE_NAME = 'answer.json'
CODENATION_TOKEN = os.getenv('CODENATION_TOKEN')
URL_GENERATE_DATA = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data'
URL_SUMBIT_SOLUTION = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution'


def main():
    data = get_generated_data()
    save_json_file(FILE_NAME, data)

    data['decifrado'] = decrypt_string(data['cifrado'], data['numero_casas'])
    save_json_file(FILE_NAME, data)

    data['resumo_criptografico'] = generate_sha1_hash(data['decifrado'])
    save_json_file(FILE_NAME, data)

    result = send_answer(FILE_NAME)
    print(result)


def get_generated_data():
    params = {'token': CODENATION_TOKEN}
    r = requests.get(url=URL_GENERATE_DATA, params=params)

    return r.json()


def save_json_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)


def decrypt_string(message, offset):
    decrypted = ''
    for c in message:
        ascii_value = ord(c)
        if ascii_value < 97 or ascii_value > 122:
            decrypted += c
            continue

        new_ascii_value = ascii_value - offset
        if new_ascii_value < 97:
            new_ascii_value += 26

        decrypted += chr(new_ascii_value)

    return decrypted


def generate_sha1_hash(string):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def send_answer(file_name):
    params = {'token': CODENATION_TOKEN}
    files = {'answer': (FILE_NAME, open(FILE_NAME, 'rb'))}
    r = requests.post(url=URL_SUMBIT_SOLUTION, params=params, files=files)

    return r.json()


if __name__ == "__main__":
    main()
