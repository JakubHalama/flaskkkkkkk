from flask import Blueprint, render_template, redirect, url_for, flash
from app import db_manager, login_manager
from .models import User, Uzivatele, Filmy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('routes', __name__)

# Alias pro databázi
db = db_manager.session

# Formulář pro přidávání filmů
class FilmForm(FlaskForm):
    nazev = StringField('Title:', validators=[InputRequired(message="Title is required"), Length(max=100)])
    rok_vydani = StringField('Year of publishment:', validators=[InputRequired(message="Director is required"), Length(max=100)])
    popis_filmu = StringField('Director:', validators=[InputRequired(message="Description is required"), Length(max=1000)])

# Routu pro přidání filmů
@bp.route("/add_filmy", methods=["GET", "POST"])
def film():
    form = FilmForm()
    if form.validate_on_submit():
        new_film = Filmy(
            nazev=form.nazev.data,
            rok_vydani=form.rok_vydani.data,
            popis_filmu=form.popis_filmu.data
        )
        db.add(new_film)
        db.commit()
        flash("Film byl úspěšně přidán.", "success")
    filmy_list = Filmy.query.all()
    return render_template("film.html", form=form, filmy=filmy_list)

# Routu pro mazání filmů
@bp.route("/delete_film/<int:film_id>", methods=["POST"])
def delete_film(film_id):
    film = Filmy.query.filter_by(id=film_id).first()
    if not film:
        flash("Film nenalezen.", "danger")
        return redirect(url_for("routes.film"))

    db.delete(film)
    db.commit()
    flash(f"Film '{film.nazev}' byl úspěšně smazán.", "success")
    return redirect(url_for("routes.film"))


# Správa databáze při každém požadavku
@bp.before_app_request
def before_request():
    db()

@bp.teardown_app_request
def shutdown_session(response_or_exc):
    db.remove()

# Správa uživatelů
@login_manager.user_loader
def load_user(user_id):
    if user_id and user_id != "None":
        return User.query.filter_by(user_id=user_id).first()
