import sys

import pandas as pd
from classifier_model.config.core import config
from classifier_model.predict import make_prediction
from classifier_model.preprocessing.data_manager import load_dataset
from classifier_model.preprocessing.get_data import download_data
from classifier_model.split_data import split_train_test_data

from my_app.config import PACKAGE_ROOT


def output_predictions() -> None:
    download_data()
    split_train_test_data()

    test_set = load_dataset(file_name=config.app_config.test_data)
    result = make_prediction(input_data=test_set, proba=True)

    predictions = result.get("predictions")[:100]
    predictions = pd.DataFrame(data=predictions, columns=["score"])

    py_ver = "pyver" + str(sys.version_info[0]) + str(sys.version_info[1])
    save_file = (
        PACKAGE_ROOT
        / "tests"
        / "differential"
        / "pred_data"
        / f"{py_ver}_pred_output.csv"
    )
    predictions.to_csv(save_file, index=False)


if __name__ == "__main__":
    output_predictions()
