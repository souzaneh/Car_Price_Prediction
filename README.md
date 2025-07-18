🚗 Car Price Prediction from TrueCar Data

📌 Project Overview

This project demonstrates how to scrape used car data from TrueCar and build a Machine Learning model to predict car prices based on features like name, year, mileage, and condition. It includes the full workflow: data extraction, storage, preprocessing, and modeling.


---

🔍 Key Features

Web Scraping: Extracts car details such as price, year, mileage, and accident history using requests and BeautifulSoup.

Database Storage: Saves scraped data in a MySQL database.

Data Preprocessing: Handles missing values, applies transformations, and encodes categorical variables.

ML Pipeline: Implements a scikit-learn pipeline with:

ColumnTransformer for numeric and categorical features

Imputation, Scaling, and Encoding


Modeling: Linear Regression for price prediction.

Evaluation: Performance measured using Mean Absolute Error (MAE) and R² score.



---

🛠️ Tech Stack

Programming Language: Python 3.x

Libraries:

requests, beautifulsoup4 for web scraping

pandas, numpy for data manipulation

matplotlib for visualization

scikit-learn for ML pipeline and modeling


Database: MySQL (mysql-connector-python)



---

📂 Project Structure

car-price-prediction/
│
├── final_project_car_price_predict.py   # Main script
├── README.md                            # Documentation
└── requirements.txt                     # Python dependencies


---

⚙️ Installation

1. Clone the repository:

git clone https://github.com/your-username/car-price-prediction.git
cd car-price-prediction


2. Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate


3. Install dependencies:

pip install -r requirements.txt


4. Set up MySQL database:

Create a database named truecar_db.

Update MySQL credentials in the script if needed.





---

▶️ How to Run

1. Ensure MySQL server is running.


2. Run the Python script:

python final_project_car_price_predict.py




---

📈 Model Performance

Training MAE: Printed in script output.

Test MAE: Printed in script output.

R² Score: Printed in script output.



---

✅ Future Enhancements

Add advanced models (RandomForest, XGBoost, etc.)

Perform hyperparameter tuning.

Deploy via Flask/Django as a web API.

Host on cloud for real-time predictions.



---

🖼️ Screenshots

(Add plots or sample outputs if available)


---

👩‍💻 Author

Suzaneh Sehati
GitHub | LinkedIn
