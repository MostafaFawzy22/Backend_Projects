# app.py
import os
import secrets
from tkinter import Image
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, logout_user, current_user, login_user
from Form import *
from PIL import Image

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Import models
from models import *
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 
   
# Routes
def save_picture(form_picture):

  image = request.files['picture']

  # Create a dictionary of folders to save images to, based on their filenames.
  folders = {
    'series': 'static/images/series/',
    'movies': 'static/images/movies/',
    'anime': 'static/images/anime/',
    'images': 'static/',
  }

  # Get the folder to save the image to, based on its filename.
  folder = folders.get(form_picture.split('.')[0], 'static/images/')

  # Create the folder if it does not exist.
  if not os.path.exists(folder):
    os.makedirs(folder)

  # Save the image to the folder.
  image.save(os.path.join(folder, form_picture))

  return form_picture



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/movies')
def movies():
    movies = Video.query.filter_by(type_video="movies").all()
    return render_template('movies.html',movies=movies)

@app.route('/series')
def series():
    series = Video.query.filter_by(type_video="series").all()
    return render_template('series.html',series=series)

@app.route('/anime')
def anime():
    anime = Video.query.filter_by(type_video="anime").all()
    return render_template('anime.html',anime=anime)

@app.route('/events')
def events():
    return render_template('events.html')
@app.route('/About_us')
def About_us():
    return render_template('index.html')

@app.route('/jw1')
def jw1():
    return render_template('jw1.html')

@app.route('/hotd')
def hotd():
    return render_template('hotd.html')

@app.route('/aot')
def aot():
    return render_template('aot.html')

@app.route('/aiw')
def aiw():
    return render_template('aiw.html')

@app.route('/Chernoby')
def Chernoby():
    return render_template('Chernoby.html')

@app.route('/jw4')
def jw4():
    return render_template('jw4.html')

@app.route('/moet')
def moet():
    return render_template('moet.html')

@app.route('/tlou')
def tlou():
    return render_template('tlou.html')

@app.route('/interstellar')
def interstellar():
    return render_template('interstellar.html')

@app.route("/add_film", methods=["GET", "POST"])
@login_required
def add_film():
    video_form = VideoForm()
    if video_form.validate_on_submit():
        print(video_form.picture.data.filename)
        if video_form.picture.data:
            picture_file = save_picture(f'{video_form.picture.data.filename}')
            # Save the picture file to the appropriate location
        film = Video(name=video_form.name.data,type_video=video_form.type_video.data,image_file=f"images/{video_form.picture.data.filename}") # type: ignore
        # Save the changes made to the certificate
        db.session.add(film) # type: ignore
        db.session.commit() # type: ignore
        return redirect(url_for("add_film"))
    
    return render_template("add_Film.html", title="Add Film", form=video_form)

    
@app.route("/edit_film", methods=["GET", "POST"])
@login_required
def edit_film():
    film = Video.query.filter_by(name='Computer Science_2').first()
    profile_form = UpdateFilmForm(obj=film)
    if film is None:
        print("film is none")
        return render_template("edit_film.html", title="Edit Film Events",profile_form=profile_form)


    if profile_form.validate_on_submit():
        print('profile validate')
        if profile_form.picture.data:
             if profile_form.picture.data.filename:
                print('profile_form.picture.data',profile_form.picture.data.filename)
                picture_file = save_picture(profile_form.picture.data.filename)
        film.image_file = profile_form.picture.data.filename
        film.name = profile_form.name.data
        film.type_video = profile_form.type_video.data
        db.session.commit() # type: ignore
        flash("Film details updated successfully", "success")
        return redirect(url_for("edit_film"))

    image_file = url_for("static", filename=f"images/{film.image_file}").replace("%0D%0A", "")
    print(image_file)
    return render_template(
        "edit_film.html",
        title="Edit Film",
        profile_form=profile_form,
        image_file=image_file,
    )


    

@app.route("/add_events", methods=["GET", "POST"])
@login_required
def add_events():
    video_form = Video_NameForm()
    if video_form.validate_on_submit():
        print("Validate True")
        print(video_form.picture.data.filename)
        if video_form.picture.data:
            picture_file = save_picture(video_form.picture.data.filename)
            # Save the picture file to the appropriate location
        film = Video_Name(type_video=video_form.type_video.data,image_file=f"images/{video_form.picture.data.filename}") # type: ignore
        # Save the changes made to the certificate
        db.session.add(film) # type: ignore
        db.session.commit() # type: ignore
        return redirect(url_for("add_events"))
    
    return render_template("add_events.html", title="Add Film Events", form=video_form)


# Users

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # type: ignore
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(full_name=form.full_name.data, email=form.email.data, password=hashed_password) # type: ignore
        if User.query.filter_by(email=user.email).first() is None:
            db.session.add(user) # type: ignore
            db.session.commit() # type: ignore
            flash(f'Account created successfully for {form.full_name.data}', 'success')
            return redirect(url_for('login'))
        else:
            flash('Account already exists', 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # type: ignore
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check credentials', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    print(current_user)
    profile_form = UpdateProfileForm()
    if profile_form.validate_on_submit():
        if profile_form.picture.data:
            if profile_form.picture.data.filename:
                print('profile_form.picture.data',profile_form.picture.data.filename)
                picture_file = save_picture(profile_form.picture.data.filename)
            current_user.image_file = profile_form.picture.data.filename
            current_user.full_name = profile_form.full_name.data
            current_user.email = profile_form.email.data
            current_user.bio = profile_form.bio.data
            db.session.commit() # type: ignore
            print(current_user)
            flash("Your profile has been updated", "success")
            return redirect(url_for("profile"))
        else:
            print(current_user)
            current_user.full_name = profile_form.full_name.data
            current_user.email = profile_form.email.data
            current_user.bio = profile_form.bio.data
            db.session.commit() # type: ignore
            flash("Your profile has been updated", "success")
            return redirect(url_for("profile"))
        
    elif request.method == "GET":
        profile_form.full_name.data = current_user.full_name # type: ignore
        profile_form.email.data = current_user.email # type: ignore
        profile_form.bio.data = current_user.bio # type: ignore
    image_file = url_for("static", filename=f"images/{current_user.image_file}").replace("%0D%0A","") # type: ignore
    return render_template(
        "dashboard.html",
        title="Profile",
        profile_form=profile_form,
        image_file=image_file,
        active_tab="profile",
    )


if __name__ == '__main__':
    app.run(debug=True)