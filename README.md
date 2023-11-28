# Fashion Recommendation System with Chatbot Integration and Image Recognition

## Overview

This project implements a sophisticated Fashion Recommendation System that harnesses the power of Natural Language Processing (NLP) and Image Recognition. It leverages Django, a high-level Python web framework, to create a user-friendly interface that recommends fashion products based on user prompts and uploaded images.

### Features

- **Chatbot Integration:** Utilizes NLP to interact with users and understand their preferences through conversational prompts.
- **Image Recognition:** Employs a ResNet model to analyze and recognize fashion items from user-uploaded images.
- **Personalized Recommendations:** Recommends fashion products tailored to individual preferences inferred from user input.

## Getting Started

To run the Fashion Recommendation System locally:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/vjsujal/Recommendation_System
    ```

2. **Setup Virtual Environment:**

    ```bash
    cd fashion-recommendation
    python -m venv venv
    source venv/bin/activate  # For Unix or MacOS
    # Or
    venv\Scripts\activate  # For Windows
    ```
3. **Download Pickle files in data folder:**

    ```bash
    cd data
    ```
    Download the file from the below link and Unzip it.
    ```bash
    https://bit.ly/pickle-file
    ```
    ```bash
    cd ..
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Server:**

    ```bash
    python manage.py runserver
    ```

5. **Access the Application:**

    Open a web browser and go to `http://localhost:8000` to access the Fashion Recommendation System.

## Usage

1. **User Input via Chatbot:**

    - Users can interact with the chatbot by entering prompts related to their fashion preferences (e.g., "I need a dress for a wedding," "Show me casual shoes").
    - The system uses NLP techniques to understand user intent and provides tailored recommendations accordingly.

2. **Image Upload for Recommendations:**

    - Users can also upload images of fashion items.
    - The system employs a ResNet model to recognize items in the image and suggests similar products available in the inventory.

## Technologies Used

- **Python:** Core language used for backend development.
- **Django:** Web framework for building the application.
- **Natural Language Processing (NLP):** Algorithms and models used to understand user input.
- **ResNet Model:** Utilized for image recognition and product recommendation.

## Contributors

- Sujal Vijayvargiya (https://github.com/vjsujal)
- Md. Ehtesham Andari (https://github.com/mdehteshamansari)
- Partha Pratim Paul (https://github.com/Real-Partha)
- Adnan Khan (https://github.com/Adnankhan0999)
