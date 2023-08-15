from flask import Flask, render_template, request, redirect, session

@app.route("/recipes")
def recipes():
    return render_template("/users/recipes.html", current_page='recipes')