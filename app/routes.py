from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.gigapi import get_recipe

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/submit', methods=['POST'])
def submit():
    products = request.form.get('products')

    recipe = get_recipe(products)

    return {"recipe": recipe}
