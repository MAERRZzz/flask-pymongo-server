from flask import Flask, jsonify
import pymongo
import rsa

app = Flask(__name__)
mongo = pymongo.MongoClient(
    "mongodb+srv://MAERZ:maerz@maerz.snbeycr.mongodb.net/?retryWrites=true&w=majority")
db = mongo.cepu_qr


@app.route("/<string:displayName>/<string:email>/<string:id>/<path:photoUrl>")
# @app.route("/")
def home_page(displayName, email, id, photoUrl): #displayName, email, id, photoUrl
    user = list(db.user.find({"email": email}, {'private_key': 0}))

    if not user:
        public_key, private_key = rsa.newkeys(1024)
        public_key = public_key.save_pkcs1().decode('utf-8').replace("-----BEGIN RSA PUBLIC KEY-----", "").replace(
            "-----END RSA PUBLIC KEY-----", "").replace("\n", "")
        private_key = private_key.save_pkcs1().decode('utf-8').replace("-----BEGIN RSA PRIVATE KEY-----", "").replace(
            "-----END RSA PRIVATE KEY-----", "").replace("\n", "")

        try:
            db.user.insert_one({"displayName": displayName, "email": email, "id": id,
                                "photoUrl": photoUrl, "public_key": public_key, "private_key": private_key})
            print(f'Записан в БД: {email}')
            user = list(db.user.find({"email": email}, {'private_key': 0}))[0]
        except:
            print(f'Ошибка при записи.')

    else:
        user = user[0]
        print(f'Есть в БД:\n{user}')

    return jsonify({'displayName': user['displayName'], 'email': user['email'], 'photoUrl': user['photoUrl'],
                    'public_key': user['public_key']})
    # return "YES"


if __name__ == '__main__':
    app.run(debug=True)
