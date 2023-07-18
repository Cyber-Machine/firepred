from flask import Blueprint, render_template, request

from firepred.pipeline.predict_pipeline import PredictPipeline

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")


@predict_bp.route("", methods=["POST", "GET"])
def predict():
    pipeline = PredictPipeline()

    try:
        int_features = [[int(x) for x in request.form.values()]]

    except Exception:
        return render_template(
            "forest_fire.html",
            error="Input values are less",
        )

    if any(feature < 0 or feature > 100 for feature in int_features[0]):
        return render_template(
            "forest_fire.html",
            error="Invalid Input, values must be in range from [0, 100]",
        )

    try:
        prediction = pipeline.predict(int_features)
        print(prediction)
        output = "{0:.{1}f}".format(prediction[0][1], 2)

    except Exception as e:
        print(e)
        render_template("forest_fire.html", pred="There seems some error")

    if output > str(0.5):
        return render_template(
            "forest_fire.html",
            pred=f"""
                Your Forest is in Danger.
                Probability of fire occuring is {output}
                """,
            error="",
        )

    return render_template(
        "forest_fire.html",
        pred=f"""
            Your Forest is safe.Probability of fire occuring is {output}
            """,
        error="",
    )


class InputException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv
