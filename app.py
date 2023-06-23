from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

with open("models/log_reg.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return render_template("forest_fire.html")


@app.route("/predict", methods=["POST", "GET"])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final = [np.array(int_features)]
    print(int_features)
    print(final)
    prediction = model.predict_proba(final)
    output = "{0:.{1}f}".format(prediction[0][1], 2)

    if output > str(0.5):
        return render_template(
            "forest_fire.html",
            pred=f"Your Forest is in Danger.\nProbability of fire occuring is {output}",
        )

    return render_template(
        "forest_fire.html",
        pred=f"Your Forest is safe.\n Probability of fire occuring is {output}",
    )


if __name__ == "__main__":
    app.run(debug=True)
