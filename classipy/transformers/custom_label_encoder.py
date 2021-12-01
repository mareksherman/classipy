import joblib
from sklearn.preprocessing import LabelEncoder
import os.path


class CustomLabelEncoder:
    def __init__(self) -> None:
        path_to_encoder = os.path.join(
            os.path.dirname(__file__), 'LabelEncoder.joblib')

        encoder = LabelEncoder = joblib.load(path_to_encoder)
        self.classes_ = encoder.classes_
        self.encoder = encoder

    def transform(self, y):
        return self.encoder.transform(y)

    def inverse_transform(self, y):
        return self.encoder.inverse_transform(y)
