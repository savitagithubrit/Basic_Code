# from flask import Flask, jsonify
# from pgconn.db_conn import SessionLocal
# from pgconn.table import Flipkart, Amazon

# app = Flask(__name__)
# app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# # Database session dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         return db
#     finally:
#         db.close()


# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({"message": "API is running successfully 🚀"})


# # API — /flipkart OR /amazon
# @app.route("/<site>", methods=["GET"])
# def get_products(site):
#     db = get_db()
#     site = site.lower()

#     if site == "flipkart":
#         data = db.query(Flipkart).all()
#         return jsonify({
#             "site": "flipkart",
#             "total_products": len(data),
#             "products": [{k: v for k, v in item.__dict__.items() if k != "_sa_instance_state"} for item in data]
#         })

#     elif site == "amazon":
#         data = db.query(Amazon).all()
#         return jsonify({
#             "site": "amazon",
#             "total_products": len(data),
#             "products": [{k: v for k, v in item.__dict__.items() if k != "_sa_instance_state"} for item in data]
#         })

#     else:
#         return jsonify({"error": "Invalid site. Use '/flipkart' or '/amazon'."})


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, jsonify
from pgconn.db_conn import SessionLocal
from pgconn.table import Flipkart, Amazon

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# ---------- DB SESSION ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- MODEL SELECTOR ----------
def get_model(model):
    if not model:
        return None
    model = model.lower()
    if model == "flipkart":
        return Flipkart
    if model == "amazon":
        return Amazon
    return None

# ---------- HOME ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running successfully 🚀"})

# ---------- READ ONE PRODUCT ----------
@app.route("/product", methods=["GET"])
def read_one():
    db = next(get_db())
    model = request.args.get("model")
    pid = request.args.get("id")

    if not model or not pid:
        return jsonify({"error": "Provide ?model=amazon or flipkart & ?id=number"}), 400

    try:
        pid = int(pid)
    except ValueError:
        return jsonify({"error": "Invalid id, must be a number"}), 400

    Model = get_model(model)
    if not Model:
        return jsonify({"error": "Invalid model name"}), 400

    item = db.query(Model).filter(Model.id == pid).first()
    if not item:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({k: v for k, v in item.__dict__.items() if k != "_sa_instance_state"})

# ---------- READ ALL PRODUCTS ----------
@app.route("/products", methods=["GET"])
def read_all():
    db = next(get_db())
    model = request.args.get("model")

    if not model:
        return jsonify({"error": "Provide ?model=amazon or flipkart"}), 400

    Model = get_model(model)
    if not Model:
        return jsonify({"error": "Invalid model name"}), 400

    data = db.query(Model).all()
    return jsonify([
        {k: v for k, v in row.__dict__.items() if k != "_sa_instance_state"}
        for row in data
    ])

# ---------- CREATE PRODUCT ----------
@app.route("/product", methods=["POST"])
def create():
    db = next(get_db())
    model = request.args.get("model")

    if not model:
        return jsonify({"error": "Provide ?model=amazon or flipkart"}), 400

    Model = get_model(model)
    if not Model:
        return jsonify({"error": "Invalid model name"}), 400

    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    new_item = Model(**data)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return jsonify({
        "message": "Product added",
        "data": {k: v for k, v in new_item.__dict__.items() if k != "_sa_instance_state"}
    })

# ---------- UPDATE PRODUCT ----------
@app.route("/product", methods=["PUT"])
def update():
    db = next(get_db())
    model = request.args.get("model")
    pid = request.args.get("id")

    if not model or not pid:
        return jsonify({"error": "Provide ?model=xyz & ?id=number"}), 400

    try:
        pid = int(pid)
    except ValueError:
        return jsonify({"error": "Invalid id, must be a number"}), 400

    Model = get_model(model)
    if not Model:
        return jsonify({"error": "Invalid model"}), 400

    item = db.query(Model).filter(Model.id == pid).first()
    if not item:
        return jsonify({"error": "Product not found"}), 404

    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    for k, v in data.items():
        if hasattr(item, k):
            setattr(item, k, v)

    db.commit()
    db.refresh(item)

    return jsonify({
        "message": "Product updated",
        "data": {k: v for k, v in item.__dict__.items() if k != "_sa_instance_state"}
    })

# ---------- DELETE PRODUCT ----------
@app.route("/product", methods=["DELETE"])
def delete():
    db = next(get_db())
    model = request.args.get("model")
    pid = request.args.get("id")

    if not model or not pid:
        return jsonify({"error": "Provide ?model=xyz & ?id=number"}), 400

    try:
        pid = int(pid)
    except ValueError:
        return jsonify({"error": "Invalid id, must be a number"}), 400

    Model = get_model(model)
    if not Model:
        return jsonify({"error": "Invalid model"}), 400

    item = db.query(Model).filter(Model.id == pid).first()
    if not item:
        return jsonify({"error": "Product not found"}), 404

    db.delete(item)
    db.commit()

    return jsonify({"message": "Product deleted successfully"})

# ---------- MAIN ----------
if __name__ == "__main__":
    app.run(debug=True)
