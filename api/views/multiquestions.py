from api import app
from flask import jsonify, request, make_response

import api.models.multiquestion as Multi

# Full path for the URL
URL_VERSION = app.config["URL_VERSION"]

# Route responsible for listing all multiquestions (GET) 
# and also for adding new ones.
# TODO: Create filter when listing. By TAG and also by TYPE, or both at same
@app.route(f"{URL_VERSION}/multiquestion/list", methods=['GET'])
@app.route(f"{URL_VERSION}/multiquestion/list/<tag>", methods=['GET'])
def multiquestion_list(tag="all"):
    if tag == "all":
        query = Multi.Questions.query.order_by(Multi.Questions.creation.desc()).all()
        return jsonify(multiquestion=[Multi.Questions.serialize(q) for q in query])
    
    # query = Multi.Tags.query.filter_by(tagname=tag).all()

    if len(tag) > 2:
        search = f"%{tag}%"
        query = Multi.Tags.query.filter(Multi.Tags.tagname.ilike(search)).all()

        # TODO: !!!! IMPORTANT !!! CORRECT THIS  <------------------ YOU CAN DO BETTER
        multiquestion = []
        for i in query:
            mq = {}
            for o in i.question:
                mq['uuid'] = o.uid
                mq['id'] = o.id
                mq['question'] = o.question
                mq['options'] = [o.option1, o.option2, o.option3, o.option4]
                mq['score'] = o.score
            multiquestion.append(mq)
        # ----------- MARSHMALLOW IT

        return jsonify(multiquestion=multiquestion)
    return jsonify(multiquestion="")


# TODO: Should have a look at the serialization 
@app.route(f"{URL_VERSION}/multiquestion/search/<string>", methods=['GET'])
def multiquestion_search(string):
    if len(string) > 4:
        search = f"%{string}%"
        query = Multi.Questions.query.filter(Multi.Questions.question.ilike(search)).all()
        return jsonify(multiquestion=[Multi.Questions.serialize(q) for q in query])

    return jsonify(multiquestion="")


# TODO: Please, in the future change the request to accept on JSON
@app.route(f"{URL_VERSION}/multiquestion/add", methods=['POST'])
def multiquestion_add():
    res = request.form
    question = Multi.Questions(
        correct = res.get("correct"),
        option1 = res.get("opt1"),
        option2 = res.get("opt2"),
        option3 = res.get("opt3"),
        option4 = res.get("opt4"),
        question = res.get("question"),
        score = res.get("score")
    )

    tags = res.get("tags").split(" ")
    for tag in tags:
        t = tag.lower()
        # Validate if tag exist on the database
        check = Multi.Tags.query.filter(Multi.Tags.tagname==t).first()
        if check:
            # TODO: Need to validate how to add new relationship to an existing value on the table
            # OBS: I dont want duplicate tags in the same table, please think
            pass
        else:
            add_tag = Multi.Tags(tagname=t, question=[question])
            Multi.db.session.add(add_tag)
            
    types = {}
    qtype = Multi.Types.query.distinct(Multi.Types.type).all()
    for q in qtype:
        typename = res.get(q.type)
        add_type = Multi.Types(type=q.type, typename=typename, question=[question])
        types[q.type] = typename
        Multi.db.session.add(add_type)

    # Dealing with media
    # TODO: Compress images using Pillow, but in-memory. Have a look at StringIO
    # TODO: Perhaps change the model and create thumbnails field. Just an idea :)
    file = request.files.get("media")
    if (file):
        add_media = Multi.Media(filetype=file.content_type, data=file.read(), question=[question])
        Multi.db.session.add(add_media)
    #
    
    if Multi.db.session.commit():
        return make_response(jsonify(question, types, tags), 200)
    else:
        answer = {}
        answer['status'] = 'Format Error'
        return make_response(jsonify(message=answer), 400)