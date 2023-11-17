from flask import Flask, jsonify, render_template, request
import os
from recommend import txt_train
import pandas as pd

app = Flask(__name__)



# Set the directory to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    user_text = request.form['message']
    user_image = request.files.get('image')  # Use get() to avoid KeyError if 'image' is not present

    if user_image:
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], user_image.filename)
        user_image.save(image_filename)
        print(f"Image saved as: {image_filename}")
    else:
        print("No image uploaded.")
        ans=txt_train(user_text)

    response = {'message': user_text}
    return render_template('index.html', response=response)



if __name__ == '__main__':
    # txt_train("purple shirt")
    app.run(debug=True)
