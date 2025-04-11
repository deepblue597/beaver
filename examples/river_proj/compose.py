
# %%
import numbers
from river.compose import Select, TransformerProduct
from river import preprocessing
from river import linear_model
from river import compose, preprocessing
import math
from pprint import pprint
import datetime as dt
from river import compose

x = {'date': '2019-02-14'}


def parse_date(x):
    date = dt.datetime.strptime(x['date'], '%Y-%m-%d')
    x['is_weekend'] = date.day in (5, 6)
    x['hour'] = date.hour
    return x


t = compose.FuncTransformer(parse_date)
pprint(t.transform_one(x))
# %%

X = [{'x': 3.14/2, 'type': "int"}, {'x': 3.14/2,
                                    'type': "float"}, {'x': 3.14/2, 'type': "str"}, {'x': 3.14/2, 'type': "str"},  {'x': 3.14/2,
                                                                                                                    'type': "float"}]
# %%


def sin(x):
    x['sin'] = math.sin(x['x'])
    return x


t = compose.FuncTransformer(sin)
for x in X:
    x = t.transform_one(x)

X

# %%


def sin(x):
    x['sin'] = math.sin(x['x'])
    return {**x, 'sin': math.sin(x['x'])}


t = compose.FuncTransformer(sin)
t.transform_one(x)

# %%
t = compose.Grouper(transformer=compose.FuncTransformer(sin), by="type")
for x in X:
    x = t.transform_one(x)

X

# %%

# Create a Grouper that applies StandardScaler to only the "temperature" feature
grouper = compose.Grouper(
    transformer=compose.Select("temperature") | preprocessing.StandardScaler(),
    by="region"
)

# Example data
data = [
    {"region": "north", "temperature": 15},
    {"region": "south", "temperature": 25},
    {"region": "north", "temperature": 16},
    {"region": "south", "temperature": 24},
]

# Learn and transform the data
for x in data:
    grouper.learn_one(x)
    transformed = grouper.transform_one(x)
    print(f"Input: {x}, Transformed: {transformed}")

# %%
scaler = preprocessing.StandardScaler()
log_reg = linear_model.LinearRegression()
model = scaler | log_reg
model
# %%
model['LinearRegression']
# %%
x = dict(
    a=0, b=1,  # group 1
    x=2, y=3   # group 2
)
# %%
x
# %%
product = TransformerProduct(
    Select('a', 'b'),
    Select('x', 'y')
)
pprint(product.transform_one(x))

# %%

mapping = {'a': 0, 'c': 'o', 'b': 1, 'd': 'p'}
x = [{'a': 42, 'b': 12},
     {'a': 42, 'c': 12},
     {'a': 42, 'd': 12},
     {'a': 42, 'b': 12, 'c': 12},
     {'a': 42, 'b': 12, 'd': 12},
     {'a': 42, 'c': 12, 'd': 12},
     {'a': 42, 'b': 12, 'c': 12, 'd': 12}]

for x in x:
    print(compose.Renamer(mapping).transform_one(x))
# %%
x
# %%

x = {'a': 42, 'b': 12}
compose.Prefixer('prefix_').transform_one(x)
# %%

x = {'a': 42, 'b': 12}
compose.Suffixer('_suffix').transform_one(x)
# %%

num = compose.SelectType(numbers.Number) | preprocessing.StandardScaler()
cat = compose.SelectType(str) | preprocessing.OneHotEncoder()
model = (num + cat) | linear_model.LogisticRegression()
# %%
model
# %%
