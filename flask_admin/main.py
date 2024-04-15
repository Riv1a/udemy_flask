from flask import render_template, url_for, redirect
from config import app, db, admin, bcrypt, login_manager
from models import Admins, Comment
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import BaseView, expose
from os.path import dirname, join
from flask_login import login_user, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return Admins.query.filter_by(id=int(user_id)).first()

class AdminView(ModelView):
    column_exclude_list = ['birthday']
    column_display_pk = True
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)
        return super().on_model_change(form, model, is_created)
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return '<h1>You are not logged in!</h1>'

class CommentView(ModelView):
    create_modal = True


class NotificationsView(BaseView):
    @expose('/')
    def indexview(self):
        return self.render('admin/notification.html')

admin.add_view(AdminView(Admins, db.session))
admin.add_view(CommentView(Comment, db.session))

path = join(dirname(__file__), 'uploads')
admin.add_view(FileAdmin(path, '/uploads', name='Uploads'))

admin.add_view(NotificationsView(name='Notifications', endpoint='notify'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    admin_user = Admins.query.filter_by(id=1).first()
    login_user(admin_user)
    return redirect(url_for('admin.index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)