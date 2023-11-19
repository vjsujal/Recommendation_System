from flask import Flask, jsonify, render_template, request
import os
from recommend import txt_train, image_test, txt_image_test
import pandas as pd
import base64

app = Flask(__name__)



# Set the directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('product.html')



@app.route('/submit_txt', methods=['POST'])
def submit_txt():
    user_text = request.get_json().get("message")
    lst=txt_train(user_text)
    response = {'item1': lst[0], 'item2': lst[1], 'item3': lst[2], 'item4': lst[3], 'item5': lst[4]}
    return jsonify(response)

@app.route('/submit_img', methods=['POST'])
def submit_img():
    uploaded_file = request.files['image'] 
    if uploaded_file.filename != '':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(image_path)
        lst=image_test(image_path)
        os.remove(image_path)
        response = {'item1': lst[0], 'item2': lst[1], 'item3': lst[2], 'item4': lst[3], 'item5': lst[4]}
    return jsonify(response)


@app.route('/submit_both', methods=['POST'])
def submit_both():
    uploaded_file = request.files['image'] 
    user_text = request.form.get('message')
    if uploaded_file.filename != '':
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(image_path)
        lst=txt_image_test(user_text,image_path)
        os.remove(image_path)
        response = {'item1': lst[0], 'item2': lst[1], 'item3': lst[2], 'item4': lst[3], 'item5': lst[4]}
    return jsonify(response)



if __name__ == '__main__':
    app.run(debug=True)
