from flask import Flask, render_template
import pymongo
import rsa

app = Flask(__name__)
mongo = pymongo.MongoClient(
    "mongodb+srv://MAERZ:maerz@maerz.snbeycr.mongodb.net/?retryWrites=true&w=majority")
db = mongo.cepu_qr


                # НОРМАЛЬНЫЙ ССЫЛКА
# @app.route("/<string:displayName>/<string:email>/<int:id>/<string:photoUrl>", methods=["GET", "POST"])
# def home_page(displayName, email, id, photoUrl):

                # ДЛЯ ТЕСТА
#   http://192.168.2.101:5000/OSMAN@mail.ru/ОСМАН/ОСМАНов


@app.route("/<string:email>/<string:first_name>/<string:last_name>", methods=["GET", "POST"])
def home_page(email, first_name, last_name):
    print(email)
    # first_name, last_name, email = "Тест", "Тестов", "test@mail.ru"
    user = list(db.user.find({"email": email}))

    if not user:
        public_key, private_key = rsa.newkeys(1024)
        public_key = public_key.save_pkcs1().decode('utf-8').replace("-----BEGIN RSA PUBLIC KEY-----", "").replace(
            "-----END RSA PUBLIC KEY-----", "").replace("\n", "")
        private_key = private_key.save_pkcs1().decode('utf-8').replace("-----BEGIN RSA PRIVATE KEY-----", "").replace(
            "-----END RSA PRIVATE KEY-----", "").replace("\n", "")

                # НОРМАЛЬНЫЙ ЗАПРОС
        # db.user.insert_one({"displayName": displayName, "email": email, "id": id,
        #                     "photoUrl": photoUrl, "public_key": public_key, "private_key": private_key})

        db.user.insert_one({"first_name": first_name, "last_name": last_name, "email": email,
                            "public_key": public_key, "private_key": private_key})
        print(f'Записан в БД: {email}')
    else:
        print(f'Есть в БД:\n{user}')

    return render_template("index.html", user_email=user)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")