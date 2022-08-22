from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

title = "TODO sample app with Flask and MongoDB"
heading = "TODO APP with Flask and MongoDB"

# client = MongoClient("mongodb://127.0.0.1:27017")
client = MongoClient("mongodb+srv://quickwork:quickwork@users.46fhmfp.mongodb.net/?retryWrites=true&w=majority")
db = client.todo_project
todos = db['todo']

def redirect_url():
    return request.args.get("next") or request.referrer or url_for("index")

@app.route("/")
def home():
    todos_1 = todos.find()
    a1 = 'active'
    return render_template('index.html', a1=a1, todos=todos_1, t=title, h=heading)



@app.route('/uncompleted')
def tasks():
    todos_1 = todos.find({"done":'no'})
    a2 = 'active'
    return render_template('uncompleted.html', a2=a2, todos=todos_1, t=title, h=heading)

@app.route('/list')
def lists():
    todos_1 = todos.find()
    a1 = 'active'
    return render_template('index.html', a1=a1, todos=todos_1, t=title, h=heading)


@app.route('/completed')
def completed():
    todos_1 = todos.find({"done":'yes'})
    a3 = 'active'
    return render_template('complete.html', a3=a3, todos=todos_1, t=title, h=heading)

@app.route("/done")
def done():
    id = request.values.get('_id')
    tasks = todos.find({'_id':ObjectId(id)})

    if(tasks[0])['done'] == 'yes':
        todos.update_one({"_id":ObjectId(id)}, {"$set":{'done':'no'}})
    else:
        todos.update_one({"_id":ObjectId(id)}, {"$set":{'done':'yes'}})
    redir = redirect_url()
    return redirect(redir)

@app.route("/action", methods=["POST"])
def action():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    todos.insert_one({"name":name, "desc":desc, "date":date, 'pr':pr, 'done':'no'})
    return redirect('/list')


@app.route("/action4", methods=["POST"])
def action4():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    todos.insert_one({"name":name, "desc":desc, "date":date, 'pr':pr, 'done':'no'})
    return redirect('/uncompleted')


@app.route("/action2", methods=["POST"])
def action2():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    todos.insert_one({"name":name, "desc":desc, "date":date, 'pr':pr, 'done':'yes'})
    return redirect('/completed')


@app.route("/remove")
def remove():
    key = request.values.get('_id')
    todos.delete_one({"_id":ObjectId(key)})
    return redirect('/list')

@app.route("/update")
def update():
    id = request.values.get('_id')
    task = todos.find({'_id':ObjectId(id)})
    return render_template('update.html', tasks=task, h=heading, t=title)

@app.route("/action3", methods=['POST'])
def action3():
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    id = request.values.get('_id')

    todos.update_one({"_id":ObjectId(id)}, {'$set':{"name":name, "desc":desc, "date":date, 'pr':pr}})
    return redirect('/list')

@app.route("/search", methods=["GET"])
def search():
    key = request.values.get('key')
    refer = request.values.get('refer')
    if(key == "_id"):
        todos_1 = todos.find({refer:ObjectId(key)})
    else:
        todos_1 = todos.find({refer:key})
    return render_template('searchlist.html', todos=todos_1, t=title, h=heading)



port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)



