from sklearn.ensemble import VotingClassifier
import os.path
import glob
import joblib

from classipy import CustomLabelEncoder

from classipy.models.heuristic import Heuristic


class CustomVotingClassifier:
    def __init__(self,user_data) -> None:
        self.user_data = user_data
        self.estimators = self.get_estimators()
        self.encoder = CustomLabelEncoder()

        pass

    def get_estimators(self):
        path_to_models = os.path.join(
            os.path.dirname(__file__), 'trained_models')
        model_files = glob.glob(path_to_models+'/*.joblib')
        models = {}
        for model_file in model_files:
            name = os.path.basename(model_file).strip('.joblib')
            model = joblib.load(model_file)
            models[name] = model

        heuristic_model = Heuristic(self.user_data)
        models['heuristic_model'] = heuristic_model
        return models

    def predict(self, X):
        estimators = [(name, model) for name, model in self.estimators.items()]
        vc = VotingClassifier(estimators, voting='soft', n_jobs=-1)
        vc.estimators_ = [est[1] for est in estimators]

        print(vc.estimators_)

        vc.le_ = self.encoder
        vc.classes_ = self.encoder.classes_

        return vc.predict(X)
