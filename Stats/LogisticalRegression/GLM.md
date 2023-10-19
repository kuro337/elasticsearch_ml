# GLM

```bash
For a GLM - first we define the Models of our Entities. 

Then we determine the Interactions possible between thhe Entities

Based on those Interactions we figure out the Features required 

1. Identify Models - User , Post , Product

2. Identify Interactions - PostVisit , UserLogin , PostLike , UserLogout , PostComment , PostShare

3. Identify Features - User , Post , Product , Interaction , Derived

```

- Illustration

```bash
# Initial Dataset

| Username | Post Title             | Gender | Country | Timestamp       | Date         | Interaction Type |
|----------|------------------------|--------|---------|-----------------|--------------|------------------|
| JohnDoe  | How to Code in Python  | Male   | USA     | 2023-10-15 09:00| 2023-10-10   | view             |
| JaneDoe  | Learn Java Basics      | Female | USA     | 2023-10-15 10:00| 2023-10-13   | comment          |
| JohnDoe  | Understanding JavaScript| Male  | USA     | 2023-10-15 11:00| 2023-10-07   | like             |
| JaneDoe  | How to Code in Python  | Female | USA     | 2023-10-15 12:00| 2023-10-10   | view             |

# Feature Engineering - Map the Data to Features such as Post Age and Viewed

| Username | Post Title              | Gender | Country | Post Age (days) | Viewed |
|----------|------------------------ |--------|---------|-----------------|--------|
| JohnDoe  | How to Code in Python   | Male   | USA     | 5               | 1      |
| JaneDoe  | Learn Java Basics       | Female | USA     | 2               | 0      |
| JohnDoe  | Understanding JavaScript| Male   | USA     | 8               | 0      |
| JaneDoe  | How to Code in Python   | Female | USA     | 5               | 1      |


# X - Features of Data

| Gender | Country | Post Age (days) |
|--------|---------|-----------------|
| Male   | USA     | 5               |
| Female | USA     | 2               |
| Male   | USA     | 8               |
| Female | USA     | 5               |


# Y - Target Variable

| Viewed |
|--------|
| 1      |
| 0      |
| 0      |
| 1      |



```
## Use Case - Recommendation System

- `GLM Use Case` : We might use logistic regression (a type of GLM) to model the probability of a user viewing a post based on the features of the user and post

- So how to achieve this?

```bash
class Interaction(BaseModel):
    
    user_username: str
    post_id: str
    interaction_type: str  # "view", "like", "comment", etc.
    timestamp: str  # ISO f

1. Identify Models - User , Post , Interaction

2. Create Indexes in ES for - User , Post , Interaction

3. We pull this data from ES - and feed it to our GLM Model

  - A python script will pull the data from ES and feed it to the GLM Model
  
```
- Once we have the Models for User , Post , and Product

- We need to do Feature Engineering

- GLM can help us provide personalization to Users

  - User's favorite Posts and Languages
  - Favorite Languages for Users with Age above a number
  - Favorite tags based on Gender
  - Favorite Posts and Languages based on Gender 
  - Depending on when a Person Logs in - which posts they view
  - User's favorite languages

- Once we have a User and a Post Model - we can come up with the Interaction Models

  - This Model will represent each Interaction between a User and a Post
  - For example - user liking a Post , user commenting on a Post , user sharing a Post

```bash
User Features
- Age
- Country
- Gender 

Post Features
- Age (time since posted)
- Author 

Interaction Features
- Number of Previous Interactions by User
- Types of Interactions 

Product Features
- Number of Previous Interactions by User for a Product
- Types of Interactions with a Product

Derived  Features
- Frequencies of Interactions by User (interactions per day)
- Ratio of likes to views for a particular user or post. 
```

- Results

```bash
# Accuracy: 1.0
# Precision: 1.0
# Recall: 1.0
# ROC-AUC: 1.0
# Model Interpretation

#                      Feature  Coefficient
# 10     interaction_type_view     1.507763
# 5                  lang_java     0.320134
# 3                gender_Male     0.064540
# 4                country_USA     0.000007
# 1              post_age_days     0.000000
# 2              gender_Female    -0.064533
# 7                lang_python    -0.064533
# 6                    lang_js    -0.255594
# 8   interaction_type_comment    -0.573402
# 0                        age    -0.575537
# 9      interaction_type_like    -0.934354

# Positive coefficients indicate a feature that increases the likelihood of viewing,
# Negative coefficients indicate a feature that decreases the likelihood.

```
### Leveraging Results

#### Real Time Predictions

- Utilizing the Model with Elasticsearch:

- When a user visits the page - we get their attributes - that we used to train the GLM 
- If GLM was trained with Gender , Age , Country , Language , Interaction Type ,- get this from the User

- 1. Gathering Attributes

- Example User Interaction

```python
# Assume these are the attributes collected during an interaction
user_attributes = {
    'age': 25,
    'gender': 'Male',
    # ... other user attributes
}
post_attributes = {
    'post_age_days': 2,
    'lang': 'java',
    # ... other post attributes
}
interaction_type = 'view'  # or 'like', 'comment', etc.

# Combine all attributes into a single feature vector
feature_vector = {**user_attributes, **post_attributes, 'interaction_type': interaction_type}


```


2. Model Scoring

- Now we have the user's fields that we know contribute to the View Probability

- Our GLM can run daily to generate the probabilities for all Posts for all Users and updates these scores in ES.

- Doing this - the scores are ready to be scored for a User

- We can store the `view_probability` in Elasticsearch as a field in the Post document

```json
{
    "post_id": "post123",
    "title": "Title of the Post",
    "user_view_probabilities": [
        {"user_id": "user1", "view_probability": 0.8},
        {"user_id": "user2", "view_probability": 0.6},
        // ... other users
    ],
    // ... other post attributes
}

```


- 3. Querying ES

- When querying ES - we can use the function_score query to adjust the ranking based on the `view_probability` for the user.

- This way, the scores are used to personalize the ranking of the search results or post feed for each user without having to re-compute the scores in real-time.



- Calculating View Probaility for User-Post and inserting to ES

```python
from elasticsearch import Elasticsearch

# Assume es is your Elasticsearch client
es = Elasticsearch()

for index, row in merged_df.iterrows():
    # Construct the feature vector from the row
    feature_vector = row[[
        'age',
        'post_age_days',
        'gender_Male',
        'gender_Female',
        'country_USA',
        'lang_js',
        'lang_java',
        'lang_python',
        'interaction_type_view',
        'interaction_type_like',
        'interaction_type_comment'
    ]].tolist()
    
    # Calculate the view probability
    view_probability = calculate_view_probability(lr, feature_vector)
    
    # Update Elasticsearch
    # Assume the document id is a combination of username and post_id
    doc_id = f'{row["username"]}_{row["post_id"]}'
    update_script = {
        "script": {
            "source": "ctx._source.view_probability = params.view_probability",
            "params": {
                "view_probability": view_probability
            }
        }
    }
    es.update(index='your_index', id=doc_id, body=update_script)


```

### Other Use Cases

- Real-Time Predictions: You can use the trained Logistic Regression model to make real-time predictions on whether a user would be interested in a post based on their previous interactions and other features. These predictions can then be used to rank the posts in Elasticsearch.

- Indexing Feature Vectors: Elasticsearch has the capability to index feature vectors. You can create a feature vector for each post based on the features used in your model, and index these vectors in Elasticsearch.

- Similarity Search: Utilizing the feature vectors, Elasticsearch can perform similarity searches to find posts that are similar to a particular post a user has interacted with, thereby providing more relevant post recommendations.

- Boosting: Elasticsearch allows for query-time boosting where certain features can be given more weight based on your model's coefficients. For instance, boosting posts with interaction_type_view or lang_java based on the positive coefficients from your model.