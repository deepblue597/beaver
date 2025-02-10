# %%
import pandas as pd
from river_proj import compose
from river_proj import feature_extraction
from river_proj import naive_bayes

docs = [
    ("Chinese Beijing Chinese", "yes"),
    ("Chinese Chinese Shanghai", "yes"),
    ("Chinese Macao", "maybe"),
    ("Tokyo Japan Chinese", "no")
]

model = compose.Pipeline(
    ("tokenize", feature_extraction.BagOfWords(lowercase=False)),
    ("nb", naive_bayes.MultinomialNB(alpha=1))
)

for sentence, label in docs:
    model.learn_one(sentence, label)

model["nb"].p_class("yes")
# %%
model["nb"].p_class("no")
# %%
model["nb"].p_class("maybe")
# %%
model.predict_proba_one("test")
# %%
model.predict_one("test")

# %%
