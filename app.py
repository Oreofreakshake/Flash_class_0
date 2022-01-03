from flask import Flask, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import messagebird

app = Flask(__name__)
app.config.from_pyfile("config_file.cfg")

client = messagebird.Client(app.config["SECRET_KEY"])

project_dir = os.path.dirname(os.path.abspath(__file__))  # gets the project directory
database_file = "sqlite:///{}".format(os.path.join(project_dir, "orderDatabase.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# Create our database model
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    phone = db.Column(db.String(128))
    items = db.Column(db.String(128))
    status = db.Column(db.String(64))

    def __repr__(self):
        return "<Customer {}>".format(self.name)


db.create_all()

db.session.query(Order).delete()


db.session.commit()


Order1 = Order(
    id="1b992e39dc55f0c79dbe613b3ad02f29",
    name="SORRY",
    phone="+9607373906",
    items="DEEZNUTS BRO",
    status="sendSMS",
)


db.session.add_all([Order1])
db.session.commit()


@app.route("/")
def index():

    table = Order.query.all()
    return render_template("index.html", table=table)


@app.route("/orderUpdate", methods=["POST"])
def update():
    try:
        newStatus = request.form.get("orderStatus")
        currentOrder = Order.query.filter_by(id=request.form.get("id")).first()
        currentOrder.status = newStatus
        db.session.commit()
    except Exception as e:
        flash("Could not update order status")
        flash(e)
    table = Order.query.all()
    return render_template("index.html", table=table)


@app.route("/notify", methods=["POST"])
def notify():
    currentOrder = Order.query.filter_by(id=request.form.get("notify_id")).first()
    msgToSend = isOrderConfirmed(currentOrder.status, currentOrder.name)
    try:
        msg = client.message_create("GAY", currentOrder.phone, msgToSend, None)
        flash(
            currentOrder.name
            + " was notified that their order is "
            + currentOrder.status
        )
    except messagebird.client.ErrorException as e:
        flash("Could not send notification")
        for error in e.errors:
            flash(error.description)
    table = Order.query.all()
    return render_template("index.html", table=table)


def isOrderConfirmed(status, recipientName):
    if status == "sendSMS":
        return (
            "GET HACKED BRO, "
            + recipientName
            + "SORRY BRO WONT HAPPEN AGAIN PLEASE FORGIVE ME BRO SORRY BRO"
        )
    elif status == "confirmed":
        return (
            "GET HACKED BRO, "
            + recipientName
            + "SORRY BRO WONT HAPPEN AGAIN PLEASE FORGIVE ME BRO SORRY BRO"
        )


if __name__ == "__main__":
    app.run()

    #need to keep mystream broooooo