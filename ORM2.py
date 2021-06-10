from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


engine = create_engine("sqlite:///Tweets.db", connect_args={"check_same_thread": False})
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "user"

    # Columns
    id = Column("id", Integer, primary_key=True)
    id_user = Column("id_user", Integer)
    nom_user = Column("nom_user", String(500))
    nombre_followers = Column("nombre_followers", Integer)
    nombre_profils_suivi = Column("nombre_profils_suivi", Integer)
    ratio_followers_suivi = Column("ratio_followers_suivi", Integer)
    frequence_publication_tweet = Column("frequence_publication_tweet", Float)
    nombre_moyen_url = Column("nombre_moyen_url", Float)
    nombre_moyen_hashtag = Column("nombre_moyen_hashtag", Float)
    nombre_moyen_mentions = Column("nombre_moyen_mentions", Float)
    nombre_moyen_retweets = Column("nombre_moyen_retweets", Float)
    nombre_reponses = Column("nombre_reponses", Float)
    longueur_moyenne_tweet = Column("longueur_moyenne_tweet", Float)
    agressivite = Column("agressivite", Float)
    visibilite = Column("visibilite", Float)

    def __repr__(self):
        return f"<User({self.id_user()})>"

class Tweet(Base):
    __tablename__ = "tweet"

    # Columns
    id = Column("id", Integer, primary_key=True)
    id_user = Column("id_user", Integer)
    name_user = Column("name_user", String(500))
    friends_count = Column("friends_count", Integer)
    followers_count = Column("followers_count", Integer)
    text = Column("text", String(500))
    hashtags = Column("hashtags", String(500))
    urls = Column("urls", String(1000))
    fav = Column("fav", Integer)
    user_mentions = Column("user_mentions", String(500))
    timestamp = Column("timestamp", Integer)


    def __repr__(self):
        return f"<User({self.id_user()})>"

Base.metadata.create_all()
session = Session()
if __name__ == "__main__":
    print(session)
    session.commit()