import math
import os

import pandas as pd
import pytest
from classifier_model.predict import make_prediction

from my_app.config import PACKAGE_ROOT


@pytest.mark.differential
def test_predictions_differential(*, test_data: pd.DataFrame) -> None:

    current_model = make_prediction(input_data=test_data, proba=True).get(
        "predictions"
    )[:100]

    out_dir = PACKAGE_ROOT / "tests" / "differential" / "pred_data"
    other_ver_preds = []
    for file in os.listdir(out_dir):
        if file.startswith("pyver"):
            preds = pd.read_csv(out_dir / file)
            other_ver_preds.append(preds["score"].values[:100])

    assert len(other_ver_preds) > 0
    for previous_model in other_ver_preds:
        assert len(previous_model) == len(current_model)
        for a, b in zip(current_model, previous_model):
            assert math.isclose(a, b, rel_tol=0.01)
