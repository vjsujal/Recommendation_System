from flask import Flask, jsonify, render_template, request
import os
from recommend import txt_train, image_test, txt_image_test, get_info, get_random, get_info_home
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
    arr=get_random()
    lst1=[]
    for i in arr:
        lst1.append(get_info_home(i))
    return render_template('index.html', lst=lst1)
    # return render_template('index.html')




@app.route('/view_item/<item_id>')
def view_item(item_id):
    item_info = get_info(int(item_id))
    return render_template('product.html', item_info=item_info)

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
