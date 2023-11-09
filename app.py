from flask import Flask, jsonify, render_template, request
import os

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
    # user_text = request.get_json().get("message")
    # print(f"User Text: {user_text}")

    # return "Data received successfully!"
    user_text = request.form['message']
    user_image = request.files['image']

    # Process the user text
    print(f"User Text: {user_text}")

    if user_image:
        # Save the uploaded image
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], user_image.filename)
        user_image.save(image_filename)
        print(f"Image saved as: {image_filename}")

    response = {'message': user_text, 'image_filename': image_filename}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
