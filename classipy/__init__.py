from os.path import isfile
from os.path import dirname

from .transformers.dataframe_transformer import DataFrameTransformer
from .transformers.json_to_model_transformer import JSONtoModelTransformer
from .transformers.custom_label_encoder import CustomLabelEncoder
from .models.voting_classifier import CustomVotingClassifier


version_file = '{}/version.txt'.format(dirname(__file__))

if isfile(version_file):
    with open(version_file) as version_file:
        __version__ = version_file.read().strip()


def say_hello():
    print('Hello World')
