# %%
import numbers
from river import compose
from river import linear_model
from river import preprocessing

num = compose.SelectType(numbers.Number) | preprocessing.StandardScaler()
cat = compose.SelectType(str) | preprocessing.OneHotEncoder()
model = (num + cat) | linear_model.LogisticRegression()

# %%
model

# %%
