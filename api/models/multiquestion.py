from api import app, db
from datetime import datetime
import uuid

#### DEBUG PURPOSES
# from flask import Flask
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'cxYFqST8YcuK6wZV6Aoy-P_JBVYXBMSUlLBV2WsCKWQ'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://lynko:lynko@localhost/academy'


# CREATE SCHEMA IF NOT EXISTS multiquestions

class Types(db.Model):
    __tablename__ = 'types'
    __table_args__ = {'schema' : 'multiquestions'}
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    type = db.Column(db.String(80), nullable=False)
    typename = db.Column(db.String(80), nullable=False)
    question = db.relationship('Questions', secondary='multiquestions.relationtypes', backref=db.backref('types', lazy='dynamic'))

relationtypes = db.Table('relationtypes', db.Model.metadata,
    db.Column('id_question', db.Integer, db.ForeignKey('multiquestions.questions.id')),
    db.Column('id_types', db.Integer, db.ForeignKey('multiquestions.types.id')),
    schema='multiquestions')

class Tags(db.Model):
    __tablename__ = 'tags'
    __table_args__ = {'schema' : 'multiquestions'}
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    tagname = db.Column(db.String(80), unique=True, nullable=False)
    question = db.relationship('Questions', secondary='multiquestions.relationtags', backref=db.backref('tags', lazy='dynamic'))

    def serialize(self):
        output = []
        for q in self.question:
            mq = {}
            mq['uid'] = q.uid  
            output.append(mq)

        return {
            'tagname' : self.tagname,
            'question' : output
        }

relationtags = db.Table('relationtags', db.Model.metadata,
    db.Column('id_question', db.Integer, db.ForeignKey('multiquestions.questions.id')),
    db.Column('id_tag', db.Integer, db.ForeignKey('multiquestions.tags.id')),
    schema='multiquestions')

class Media(db.Model):
    __tablename__ = 'media'
    __table_args__ = {'schema' : 'multiquestions'}
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    filetype = db.Column(db.String(32))
    data = db.Column(db.LargeBinary)
    question = db.relationship('Questions', secondary='multiquestions.relationmedia', backref=db.backref('medias', lazy='dynamic'))

relationmedia = db.Table('relationmedia', db.Model.metadata,
    db.Column('id_question', db.Integer, db.ForeignKey('multiquestions.questions.id')),
    db.Column('id_media', db.Integer, db.ForeignKey('multiquestions.media.id')),
    schema='multiquestions')

class Questions(db.Model):
    __tablename__ = 'questions'
    __table_args__ = {'schema' : 'multiquestions'}
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    uid = db.Column(db.String(32), default=uuid.uuid4().hex)

    creation = db.Column(db.DateTime, default=datetime.utcnow)
    question = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    option3 = db.Column(db.Text, nullable=False)
    option4 = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    correct = db.Column(db.Text, nullable=False)

    def serialize(self):
        return {
            'id' : self.id,
            'uuid' : self.uid,
            'creation' : f"{self.creation.day}-{self.creation.month}-{self.creation.year}",
            'question' : self.question,
            'options' : [self.option1, self.option2, self.option3, self.option4],
            'score' : self.score
        }



# db.drop_all()
# db.create_all()

# insert = Questions(
#     question = 'Question',
#     option1 = 'Answer1',
#     option2 = 'Answer2',
#     option3 = 'Answer3',
#     option4 = 'Answer4',
#     score = 1,
#     correct = 'option2'
# )
# list_tags = ["teste", "office", "glass", "dog", "tag"]

# list_types = {
#     'level' : 'level name',
#     'exam' : 'exam teste',
#     'skill' : 'new skill',
#     'test' : 'test test',
#     'part' : 'new part',
# }

# for tag_name in list_tags:
#     new_tag = Tags(tagname=tag_name, question=[insert])
#     db.session.add(new_tag)

# for key, value in list_types.items():
#     new_type = Types(type=key, typename=value, question=[insert])
#     db.session.add(new_type)

# db.session.commit()


