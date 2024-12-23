#%% 
from river import datasets

dataset = datasets.Bikes()
dataset
# %%
x, y = next(iter(dataset))
x
# %%
for x, y in dataset:
    break
x
# %%
from river import stream

X_y = stream.iter_csv(dataset.path)
x, y = next(X_y)
x, y
# %%
X_y = stream.iter_csv(
    dataset.path,
    converters={
        'bikes': int,
        'clouds': int,
        'humidity': int,
        'pressure': float,
        'temperature': float,
        'wind': float
    },
    parse_dates={'moment': '%Y-%m-%d %H:%M:%S'},
    target='bikes'
)
x, y = next(X_y)
x, y
# %%
from sklearn import datasets

dataset = datasets.load_diabetes()

for x, y in stream.iter_sklearn_dataset(dataset):
    break

x, y
# %%
import flask

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def predict():
    payload = flask.request.json
    river_model = datasets.web_traffic()
    return river_model.predict_proba_one(payload)

# %%
predict() 
# %%
