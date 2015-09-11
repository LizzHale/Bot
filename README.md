### Who is Bob?

Wilhelm "Bobnut" DeKokosnoot (aka Bob) is a chat bot that uses natural language processing and machine learning to respond to the contextual polarity of the messages in a chatroom. Bob appears as any other user to chatroom participants. In order to do this, a client socket had to be built to send and receive messages using the Internet Chat Relay (IRC) protocol. All messages received through the socket are sent to Bob who sorts them and sends the appropriate output back.

### Statistical Classification

Programmed in Python, Bob uses a machine learning classifier to determine his response. A classifier is a system that can predict, based on training input, the classification or category of previously unknown input. In this project, when you type a message in the chatroom, Bob uses his classifier to determine the sentiment category (whether the message is "positive" or "negative") even though he has likely never seen your message before. The training input used in this classifier is a corpus of movie reviews provided by Cornell University that are categorized as either positive or negative. The first classifier used was the naive Bayes which produced a 60% accuracy rate. This means that could accurately determine the sentiment 80% of the time. Bob is currently running a Fisher classifier with 65% accuracy so he's well on his wa to matching the accuracy of human being!

### Preprocessing

To determine the category of a chatroom, message, the classifier first extracts the meaningful features from the text. In machine learning, a feature is a property of the categories being classified. This project uses words as features, but it's quite possible to use any measurable property, for instance, length of a sentence or punctuation. In order to extract the words from the text, considerable pre-processing had to be done to strip other data, such as email addresses and numbers, from the sentences. In addition, stopwords, words with little or no semantic value, had to be removed.

### More About the Classifiers

#### The naive Bayes classifier

The naive Bayes classifiers is a probabilistic classifier that assumes that the value of a feature is unrelated to the presence or absence of any other feature, meaning that it looks at each feature in isolation to determine the category. Since language does not behave in this way, the naive Bayes classifier can become confused when, say, dealing with negation. For example, phrases like "not amazing" will be difficult for the naive Bayes to deal with.

#### The Fisher classifier

Unlike the naive Bayes, the Fisher classifier takes into account the other features present in the input to arrive at a classification. Its process is much like the naive Bayes but it goes one step further by looking at the probability that the combination of features would appear in a particular category. This can help to offset an outlying feature, for instance, if there is one very positive word in an otherwise negative sentence.  


### Technology Used

- Python
- Flask
- PostgreSQL
- SQLAlchemy
- HTML
- Jinja
- Kube CSS Framework with custom elements
- JavaScript
- jQuery and Ajax
- Deployed on Heroku and monitored using New Relic

### Installation and Configuration

#### Setup with an existing database:

- Clone the repo and cd into the repo
- Create a new virtual environment and activate (you will need to install virtualenv if you don't already have it installed)
```virtualenv env & source env/bin/activate ```
- Install postgres
- Create a new database and set the DATABASE_URL environment variable
- Create the tables by running ``` python tables.py```
- Seed the database (This take approximately 3 hours) ``` python setupdata.py ```
- Create and source the .env with the following environment variables:
  - DATABASE_URL
  - PORT
  - SECRET_KEY (for the flask app)
  - NICK (IRC nickname)
  - REALNAME (IRC realname)
  - IDENT (IRC identity)
  - CHANNEL (IRC channel)
  - PATH="/path/to/postgres:$PATH" (this is necessary to locate the pg_config during installation)
- Install the requirements ``` pip install -r requirements.txt ```
- Start the web and worker processes ``` foreman start ```


### Resources
[Polarity Dataset v2.0](ttp://www.cs.cornell.edu/people/pabo/movie-review-data/) -- 1000 positive and negative processed reviews. Introduced in Pang/Lee ACL 2004. Release June 2004
