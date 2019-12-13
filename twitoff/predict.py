import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import NearestNeighbors

from .models import User
from .twitter import BASILICA

def predict_user(user1_name, user2_name, tweet_text):
    """determine which user is more likely to produce a given tweet."""

    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()

    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])

    user1_neigh = NearestNeighbors(metric='cosine').fit(user1_embeddings)
    user2_neigh = NearestNeighbors(metric='cosine').fit(user2_embeddings)

    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    tweet_embedding = np.array(tweet_embedding).reshape(1, -1)

    user1_neighdist, _ = user1_neigh.kneighbors(X=tweet_embedding, n_neighbors=1)
    user2_neighdist, _ = user2_neigh.kneighbors(X=tweet_embedding, n_neighbors=1)

    user1_neighdist = user1_neighdist[0][0]
    user2_neighdist = user2_neighdist[0][0]

    return user1_neighdist < user2_neighdist

    """user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])

    embeddings = np.vstack([user1_embeddings, user2_embeddings])

    labels = np.concatenate([np.ones(len(user1.tweets)),
                            np.zeros(len(user2.tweets))])

    log_reg = LinearSVC().fit(embeddings, labels)

    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')

    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))"""
