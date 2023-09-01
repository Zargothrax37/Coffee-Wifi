from flask import Flask, render_template, request
import pandas as pd
import json
from wtforms import Form, StringField, validators, SelectField, SubmitField

app = Flask(__name__)


# Create the input fields using wtforms tos use in the add_coffe.html file
class CoffeeForm(Form):
    cafe_name = StringField("Name", [validators.DataRequired()], render_kw={'style': 'width: 100ch'})
    cafe_location = StringField("Location", [validators.DataRequired()], render_kw={'style': 'width: 100ch'})
    cafe_open = StringField("Opening", [validators.DataRequired()], render_kw={'style': 'width: 100ch'})
    cafe_closed = StringField("Closing", [validators.DataRequired()], render_kw={'style': 'width: 100ch'})
    cafe_coffee = SelectField("Coffee Rating",
                              choices=["-", "☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"],
                              render_kw={'style': 'width: 100ch'})
    cafe_wifi = SelectField("Wifi Rating",
                            choices=["-", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                            render_kw={'style': 'width: 100ch'})
    cafe_energy = SelectField("Energy Rating",
                              choices=["-", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                              render_kw={'style': 'width: 100ch'})
    submit = SubmitField("Submit")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/Coffee")
def coffee():
    # Create a DF of the csv file and converts it into a json file to pass to coffee.html
    df = pd.read_csv("Shops.csv")
    coffee_json = df.to_json()
    x = json.loads(coffee_json)
    return render_template("coffee.html",
                           df_cafe=x)


@app.route("/add", methods=['GET', 'POST'])
def add_coffee():
    # Gets the form data from the website and writes the users input in the Shops.csv file
    form = CoffeeForm()
    if request.method == "POST":
        new_data = request.form.to_dict()
        del new_data["submit"]
        df = pd.DataFrame(new_data, index=[0])
        df.to_csv("Shops.csv", mode="a", index=False, header=False)
    return render_template("add_coffee.html",
                           form=form)


if __name__ == "__main__":
    app.run(debug=True)
