from flask import request, Flask, render_template, session, redirect, url_for
from mongo_interface import db
from bson import ObjectId
import random

app = Flask(__name__)
@app.route("/",methods=["GET"])
def main():
    if request.method == "GET":
        return render_template("homepage.html")

@app.route("/profile",methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    else:
        name = request.form["name"]
        age = float(request.form["age"])
        gender = request.form["gender"]
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        activity_level = request.form.get("activity")
        expertise = request.form.get("expertise")
        if request.form["vegan"] == "yes":
            vegan = True
        else:
            vegan = False
        if request.form["vegetarian"] == "yes":
            vegetarian = True
        else:
            vegetarian = False
        if request.form["lactose"] == "yes":
            lactose = True
        else:
            lactose = False
        if request.form["nuts"] == "yes":
            nuts = True
        else:
            nuts = False
        doc = {"name": name, "age": age, "weight": weight,
               "height": height, "activity_level": activity_level,
               "cooking_expertise": expertise, "gender": gender, "vegan": vegan,
               "vegetarian": vegetarian,
               "lactose-intolerant": lactose, "nut_allergy": nuts}
        session["doc"] = doc
        concerns = ["vegan", "vegetarian", "lactose-intolerant", "nut_allergy"]
        restrictions = []
        for i in concerns:
            if session["doc"][i] is True:
                restrictions.append(i)
        session["restrictions"] = restrictions
        db.users.insert({"name": name, "age": age, "weight": weight,
                        "height": height, "activity_level": activity_level,
                        "cooking_expertise": expertise, "gender": gender, "vegan": vegan,
                        "vegetarian": vegetarian,
                        "lactose-intolerant": lactose, "nut_allergy": nuts})
        if session["doc"]["gender"] == "male":
            bmr = (10*session["doc"]["weight"]) + (6.25*session["doc"]["height"]) - (5*session["doc"]["age"]) + 5
        elif session["doc"]["gender"] == "female":
            bmr = (10*session["doc"]["weight"]) + (6.25*session["doc"]["height"]) - (5*session["doc"]["age"]) - 161
        calories = 1.1*bmr
        if session["doc"]["activity_level"] == 0:
            calories = (bmr * 1.1)
        elif session["doc"]["activity_level"] == 1:
            calories = bmr * 1.3
        elif session["doc"]["activity_level"] == 2:
            calories = bmr * 1.53
        elif session["doc"]["activity_level"] == 3:
            calories = bmr * 1.7
        elif session["doc"]["activity_level"] == 4:
            calories = bmr * 1.9
        possible_bf = []
        list_len = len(session["restrictions"])-1
        temp = 0
        for item in db.breakfast.find():
            for restriction in session["restrictions"]:
                if item[restriction] == True:
                    temp +=1
                else:
                    continue
            if temp == len(session["restrictions"]):
                possible_bf.append(item)
        possible_l = []
        list_len = len(session["restrictions"])-1
        temp = 0
        for item in db.lunch.find():
            for restriction in session["restrictions"]:
                if item[restriction] == True:
                    temp +=1
                else:
                    continue
            if temp == len(session["restrictions"]):
                possible_l.append(item)
        possible_d = []
        list_len = len(session["restrictions"])-1
        temp = 0
        for item in db.dinner.find():
            for restriction in session["restrictions"]:
                if item[restriction] == True:
                    temp +=1
                else:
                    continue
            if temp == len(session["restrictions"]):
                possible_d.append(item)
        possible_s = []
        list_len = len(session["restrictions"])-1
        temp = 0
        for item in db.snacks.find():
            for restriction in session["restrictions"]:
                if item[restriction] == True:
                    temp +=1
                else:
                    continue
            if temp == len(session["restrictions"]):
                possible_s.append(item)
        possible_dess = []
        list_len = len(session["restrictions"])-1
        temp = 0
        for item in db.dessert.find():
            for restriction in session["restrictions"]:
                if item[restriction] == True:
                    temp +=1
                else:
                    continue
            if temp == len(session["restrictions"]):
                possible_dess.append(item)
        calorie_limit = False
        while not calorie_limit:
            breakfast = possible_bf[random.randint(0, 2)]
            lunch = possible_l[random.randint(0, 2)]
            dinner = possible_d[random.randint(0,2)]
            dessert = possible_dess[random.randint(0, 2)]
            snack = possible_s[random.randint(0,2)]
            if breakfast["calories"] + lunch["calories"] + dinner["calories"] + dessert["calories"] + snack["calories"] <= calories:
                meal_plan = {"bf": breakfast["name"], "l":lunch["name"], "s":snack["name"], "d":dinner["name"], "dess":dessert["name"]}
                links = {"bf": breakfast["url"], "l":lunch["url"], "s":snack["url"], "d":dinner["url"], "dess":dessert["url"]}
                calorie_limit = True
            else:
                continue
        return render_template("/meal_plan.html", meal_plan=meal_plan, links=links)

if __name__ == "__main__":
    #turn off this debugging stuff before production
    app.secret_key = 'secret key'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['DEBUG'] = True
    # next line: cause KeyErrors to bubble up to top level 
	#so we can see the traceback & debugger 
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run()