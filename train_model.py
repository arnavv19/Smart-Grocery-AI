import json
import joblib
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load the training data
with open("train.json", "r") as file:
    data = json.load(file)

# Count top 10 cuisines
cuisine_counts = Counter(entry["cuisine"] for entry in data)
top_cuisines = [cuisine for cuisine, _ in cuisine_counts.most_common(10)]

# Filter data to include only top 10 cuisines
filtered_data = [entry for entry in data if entry["cuisine"] in top_cuisines]

# Limit to 1000 recipes
filtered_data = filtered_data[:1000]

# Prepare X and y
X = [" ".join(entry["ingredients"]).lower() for entry in filtered_data]
y = [entry["cuisine"] for entry in filtered_data]

# Vectorize ingredients using TF-IDF
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# Train the model using Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, zero_division=0))

# Save the model and vectorizer
joblib.dump(model, "recipe_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print(f"\n✅ Model and vectorizer saved for {len(filtered_data)} recipes across top 10 cuisines.")
