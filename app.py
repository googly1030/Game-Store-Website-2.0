from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_mysqldb import MySQL
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "MysecretKey"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "signup"

mysql = MySQL(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM signupdata WHERE id = %s", (user_id,))
    userdata = cur.fetchone()
    cur.close()
    if userdata:
        return User(userdata[0])
    else:
        return None


@app.route("/")
def mainpage():
    user_id = session.get("user_id")
    username = session.get("username")
    curpage = 0
    return render_template(
        "index.html", user_id=user_id, username=username, curpage=curpage
    )


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO signupdata (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password),
        )
        mysql.connection.commit()
        cur.close()
        return redirect("/")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM signupdata WHERE username = %s", (username,))
        userdata = cur.fetchone()
        cur.close()
        if userdata and userdata[3] == password:
            user = User(userdata[0])
            login_user(user)
            session["user_id"] = userdata[0]
            session["username"] = userdata[1]
            return redirect("/")
    return render_template("login.html")


@app.route("/gamepage", methods=["GET", "POST"])
def gamepage():
    user_id = session.get("user_id")
    src = request.args.get("src")
    title = request.args.get("title")
    price = request.args.get("price")
    username = session.get("username")
    return render_template(
        "gamecontent.html",
        user_id=user_id,
        src=src,
        title=title,
        price=price,
        username=username,
    )


@app.route("/wishlist", methods=["POST", "GET"])
@login_required
def wishlist():
    if request.method == "POST":
        src = request.form.get("src")
        title = request.form.get("title")
        price = request.form.get("price")

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM wishlist WHERE user_id = %s AND title = %s",
            (session["user_id"], title),
        )
        existing_item = cur.fetchone()
        cur.close()

        if existing_item:
            flash("Item already exists in wishlist.", "warning")
        else:

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO wishlist (user_id, title, price, image_url) VALUES (%s, %s, %s, %s)",
                (session["user_id"], title, price, src),
            )
            mysql.connection.commit()
            cur.close()
            flash("Item added to wishlist successfully.", "success")

        return redirect("/wishlist")
    else:

        user_id = session.get("user_id")
        username = session.get("username")

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id, title, price, image_url FROM wishlist WHERE user_id = %s",
            (user_id,),
        )
        wishlist_items = cur.fetchall()
        print(wishlist_items)
        cur.close()

        return render_template(
            "wishlist.html",
            user_id=user_id,
            username=username,
            wishlist_items=wishlist_items,
        )


@app.route("/remove_from_wishlist", methods=["POST"])
@login_required
def remove_from_wishlist():
    item_id = request.form.get("item_id")
    if item_id:
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM wishlist WHERE id = %s AND user_id = %s",
            (item_id, session["user_id"]),
        )
        mysql.connection.commit()
        cur.close()
        flash("Item removed from wishlist successfully.", "success")
    else:
        flash("Item ID not provided.", "error")
    return redirect("/wishlist")


@app.route("/cart", methods=["POST", "GET"])
@login_required
def cart():
    if request.method == "POST":
        src = request.form.get("src")
        title = request.form.get("title")
        price = request.form.get("price")

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM cart WHERE user_id = %s AND title = %s",
            (session["user_id"], title),
        )
        existing_item = cur.fetchone()
        cur.close()

        if existing_item:
            flash("Item already exists in cart.", "warning")
        else:

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO cart (user_id, title, price, image_url) VALUES (%s, %s, %s, %s)",
                (session["user_id"], title, price, src),
            )
            mysql.connection.commit()
            cur.close()
            flash("Item added to cart successfully.", "success")

        return redirect("/cart")
    else:

        user_id = session.get("user_id")
        username = session.get("username")

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id, title, price, image_url FROM cart WHERE user_id = %s",
            (user_id,),
        )
        cart_items = cur.fetchall()
        print("cart items", cart_items)
        cur.close()
        print(cart_items)
        total_price = sum(item[2] for item in cart_items)
        return render_template(
            "cart.html",
            user_id=user_id,
            username=username,
            cart_items=cart_items,
            total_price=total_price,
        )


@app.route("/remove_from_cart", methods=["POST"])
@login_required
def remove_from_cart():
    item_id = request.form.get("item_id")
    if item_id:
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM cart WHERE id = %s AND user_id = %s",
            (item_id, session["user_id"]),
        )
        mysql.connection.commit()
        cur.close()
        flash("Item removed from cart successfully.", "success")
    else:
        flash("Item ID not provided.", "error")
    return redirect("/cart")


pagenum = None
curpage = None


@app.route("/news", methods=["POST", "GET"])
def news():
    global pagenum, curpage
    if request.method == "POST":
        pageNo = request.json.get("page")
        currentpage = request.json.get("currentPage")
        data = request.json.get("array")
        user_id = session.get("user_id")
        username = session.get("username")
        pagenum = data
        curpage = currentpage
        print(currentpage)
        return render_template(
            "newspage.html",
            user_id=user_id,
            username=username,
            data=data,
            pageNO=pageNo,
            currentpage=currentpage,
        )
    else:
        user_id = session.get("user_id")
        username = session.get("username")
        return render_template(
            "newspage.html",
            user_id=user_id,
            username=username,
            pagenum=pagenum,
            curpage=curpage,
        )


@app.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    session.clear()
    return redirect("/")


@app.route("/payment", methods=["POST", "GET"])
@login_required
def payment():
    user_id = session.get("user_id")
    price = request.args.get("price")
    src = request.args.get("src")
    title = request.args.get("title")
    cart_total_price = request.args.get("total_price")
    if cart_total_price:
        price = cart_total_price
    return render_template(
        "payment.html",
        user_id=user_id,
        price=price,
        src=src,
        title=title,
    )


if __name__ == "__main__":
    app.run(debug=True)
