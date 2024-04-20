from apps.crud.forms import UserForm
from flask import Blueprint, render_template, redirect, url_for

# Blueprintでcrudアプリを生成する
crud = Blueprint("crud", __name__, template_folder="templates", static_folder="static")


# indexエンドポイントを作成し、index.htmlを返す
@crud.route("/")
def index():
    return render_template("crud/index.html")

# dbをimportする
from apps.app import db

# Userクラスをimportする
from apps.crud.models import User


@crud.route("/sql")
def sql():
    db.session.query(User).order_by("username").all()
    return "コンソールログを確認してください"


@crud.route("/users/new", methods=["GET", "POST"])
def create_user():
    # UserFormをインスタンス化する
    form = UserForm()
    if form.validate_on_submit():
        # ユーザーを作成する
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # ユーザーを追加してコミットする
        db.session.add(user)
        db.session.commit()
        # ユーザーの一覧画面へリダイレクトする
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


@crud.route("/users")
def users():
    """ユーザの一覧を取得する"""
    users = User.query.all()
    return render_template("crud/index.html", users=users)


@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()

    # Userモデルを利用してユーザを取得する
    user = User.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # GETの場合はHTMLを返す
    return render_template("crud/edit.html", form=form, user=user)