from flask import Flask, render_template
import pymongo
import rsa

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def mongodb():
    mongo = pymongo.MongoClient(
        "mongodb+srv://MAERZ:maerz@maerz.snbeycr.mongodb.net/?retryWrites=true&w=majority")
    db = mongo.cepu_qr
    return home_page(db)


def home_page(db):
    first_name, last_name, email = "Тест", "Тестов", "test@mail.ru"
    user = list(db.user.find({"email": email}))

    if not user:
        public_key, private_key = rsa.newkeys(1024)
        public_key = public_key.save_pkcs1().decode('utf-8').replace("-----BEGIN RSA PUBLIC KEY-----", "").replace(
            "-----END RSA PUBLIC KEY-----", "").replace("\n", "")
        private_key = private_key.save_pkcs1().decode('utf-8').replace("-----BEGIN RSA PRIVATE KEY-----", "").replace(
            "-----END RSA PRIVATE KEY-----", "").replace("\n", "")

        db.user.insert_one({"first_name": first_name, "last_name": last_name, "email": email,
                            "public_key": public_key, "private_key": private_key})
        user = list(db.user.find({"email": email}))[0]
        print(f'Записан в БД: {user["email"]}')
    else:
        print(f'Есть в БД:\n{user}')

    return render_template("index.html", user_email=user)


if __name__ == '__main__':
    app.run(debug=True)