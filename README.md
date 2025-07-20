# 🥦 SmartGrocery — AI-Powered Grocery & Recipe Assistant

**SmartGrocery** is a Flask-based web app that helps you manage your kitchen smarter. It offers intelligent recipe suggestions, nutrition summaries, inventory tracking, and a shopping list — all in a sleek, modern interface.

## 🔧 Features

* 🧠 **AI-Powered Recipe Recommendations**
  Suggests dishes based on ingredients you already have using a trained ML model.

* 🮺 **Inventory Management**
  Add or delete ingredients and track your current stock.

* 🛍️ **Shopping List Manager**
  Easily add and remove items to plan your grocery trip.

* 🍎 **Nutrition Calculator**
  Automatically calculates total calories, proteins, fats, and carbs based on your current ingredients.

* 💡 **User-Friendly Interface**
  Built with Bootstrap and custom CSS (glassmorphism, emojis, and more!).

---

## 🚀 Tech Stack

| Layer            | Technology             |
| ---------------- | ---------------------- |
| Frontend         | HTML, CSS, Bootstrap   |
| Backend          | Python (Flask)         |
| Machine Learning | Scikit-learn, joblib   |
| Data Storage     | JSON files             |
| Styling          | Custom CSS + Bootstrap |

---

## ⚙️ Getting Started

Follow these steps to run the project on your local machine:

### 📦 1. Clone the repository

```bash
git clone https://github.com/your-username/smartgrocery.git
cd smartgrocery
```

### 📥 2. Install the required dependencies

```bash
pip install flask scikit-learn joblib
```

### ▶️ 3. Run the Flask application

```bash
python app.py
```

### 🌐 4. Open in your browser

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🧠 Train Your Own Model (Optional)

You can retrain the recipe classifier using your own `train.json` dataset:

```bash
python train_model.py
```

> Make sure your `train.json` has proper structure with fields like `title`, `ingredients`, and `cuisine`.



---




## ✅ To Do (Future Enhancements)

- [x] Add user recipe support  
- [x] Live nutrition summary  
- [x] Export shopping list as PDF  
- [ ] Integrate nutrition API (e.g., USDA FoodData)  
- [ ] Dark mode toggle  
- [ ] Inventory item expiry tracking  
- [ ] Smart notifications (e.g., low-stock alerts, recipe suggestions)  
- [ ] Voice command integration  
- [ ] Mobile responsive redesign  
- [ ] Multi-user support with login/authentication  
- [ ] Export data to CSV or PDF  
- [ ] Gamify nutrition goals and achievements


---

## 👩‍💼 Authors

**Riya Saraf**  
**Arnav Patel**


---

> 💡 *Good food starts with smart choices!* 🍅🥕🥦


---


