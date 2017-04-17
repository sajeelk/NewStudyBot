import tweepy, time, pickle
from data import data
from config import consumer_key, consumer_secret, access_token, access_token_secret
from sklearn import tree
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# vec = CountVectorizer()
# features = []
# labels = []
# for i in range(len(data)):
# 	features.append(data[i][0])
# 	labels.append(data[i][1])
# clf = Pipeline([('vectorizer', CountVectorizer()), ('transformer', TfidfTransformer()), ('classifier', MultinomialNB())])
# clf = clf.fit(features, labels)
# with open("clf.pkl", "wb") as f:
# 	pickle.dump(clf, f)
with open("clf.pkl", "rb") as f:
	clf = pickle.load(f)
print "Pickle Retrieved."



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

while True:
	new_studies = api.search(q="new study")
	for s in new_studies:
		if s.user.verified and (s.text[:2] != "RT") and (clf.predict([s.text])[0] == 1):
			try:
				api.retweet(s.id)
			except:
				pass
			print "Retweeted!"
			print s.text
	time.sleep(900)
