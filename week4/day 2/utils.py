from flask import Flask, request, json
from model import MLModelHandler, DLModelHandler
from time import time
from train_ml import *

app = Flask(__name__)

# assign model handler as global variable [2 LINES]
ml_handler = MLModelHandler()
dl_handler = DLModelHandlerimport unicodedata


def clean_text(text):
    text = " ".join(text.strip().split())
    output = []
    for char in text:
        cp = ord(char)
        if cp == 0 or cp == 0xFFFD or _is_control(char):
            continue
        if _is_whitespace(char):
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)


def _is_whitespace(char):
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def _is_control(char):
    if char == "\t" or char == "\n" or char == "\r":
        return False
    cat = unicodedata.category(char)
    if cat.startswith("C"):
        return True
    return False
()


@app.route("/predict", methods=["POST"])
def predict():
    # handle request and body
    body = request.get_json()
    text = body.get('text', '')
    text = [text] if isinstance(text, str) else text
    do_fast = body.get('do_fast', True)

    # model inference [2 LINES]
    if do_fast:
        predictions = ml_handler.handle(text)
    else:
        predictions = dl_handler.handle(text)

    # response
    result = json.dumps({str(i): {'text': t, 'label': l, 'confidence': c}
                         for i, (t, l, c) in enumerate(zip(text, predictions[0], predictions[1]))})
    return result

@app.route("/train", methods=["POST"])
def train():
    start_time = time.now()
    for mode in ['train','test']:
        download_data(mode)
    model, vectorizer = train_and_evaluate()
    serialization(model,vectorizer)
    response = time.now()-start_time
    result = json.dumps({f'response time(sec)': response})
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)