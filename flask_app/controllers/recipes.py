from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('newRecipe.html',user=User.get_by_id(data))

@app.route('/recipeNew',methods=['POST'])
def newRecipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = { 
        "name": request.form["name"],
        "description": request.form["description"],
        "instruction": request.form["instruction"],
        "date": request.form["date"],
        "minute": int(request.form["minute"]),
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/success')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("editRecipe.html",edit=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/recipe',methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instruction": request.form["instruction"],
        "minute": int(request.form["minute"]),
        "date": request.form["date"],
        "id": request.form['id'], 
        "user_id": session["user_id"]
    }
    Recipe.update(data)
    return redirect('/success')

@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("viewRecipe.html",recipe=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.delete(data)
    return redirect('/success')


