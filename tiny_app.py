from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Mô hình User trong database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(256), nullable=True, default='default_avatar.png')  # Thêm trường avatar
    posts = db.relationship('Post', backref='author', lazy=True)

# Mô hình Post
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Hàm kiểm tra admin
def is_admin_user():
    return current_user.is_authenticated and current_user.is_admin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_blocked:
                flash("Tài khoản của bạn đã bị khóa.", "danger")
                return render_template("login.html")
            if user.password == password:
                login_user(user)
                if user.is_admin:
                    return redirect(url_for("admin"))
                return redirect(url_for("dashboard"))
            else:
                flash("Mật khẩu không chính xác.", "danger")
        else:
            flash("Email không tồn tại.", "danger")
    return render_template("login.html")

@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    # Sắp xếp bài viết theo ID giảm dần (mới nhất ở trên)
    posts_query = Post.query.filter_by(user_id=current_user.id).order_by(Post.id.desc())
    total_posts = posts_query.count()
    posts = posts_query.paginate(page=page, per_page=per_page, error_out=False)

    dang_bai = session.get('Them', False)
    xoa = False

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if "Them" in request.form:
            session['Them'] = True
            return redirect(url_for('dashboard', page=page))
        
        if 'submit' in request.form:
            if title and content:
                new_post = Post(title=title, content=content, user_id=current_user.id)
                db.session.add(new_post)
                db.session.commit()
                flash("Đã thêm bài viết thành công.", "success")
            session['Them'] = False
            # Sau khi thêm, chuyển về trang 1 để bài mới ở đầu
            return redirect(url_for('dashboard', page=1))
        
        if 'Xoa' in request.form:
            xoa = True
        
        elif 'Xác nhận xóa' in request.form:
            post_ids = request.form.getlist('delete_id')
            print("Post IDs selected:", post_ids)
            if post_ids:
                try:
                    for post_id in post_ids:
                        post_xoa = Post.query.get(int(post_id))
                        print(f"Post {post_id}: {post_xoa}, User match: {post_xoa.user_id if post_xoa else None} == {current_user.id}")
                        if post_xoa and post_xoa.user_id == current_user.id:
                            db.session.delete(post_xoa)
                    db.session.commit()
                    flash("Đã xóa bài viết thành công.", "success")
                except Exception as e:
                    db.session.rollback()
                    flash(f"Lỗi khi xóa bài viết: {str(e)}", "danger")
            else:
                flash("Vui lòng chọn ít nhất một bài viết để xóa!", "danger")
            return redirect(url_for('dashboard', page=page))
        
        if 'Close_popup' in request.form:
            session['Them'] = False
            return redirect(url_for('dashboard', page=page))

    return render_template("dashboard.html", user=current_user, posts=posts.items, 
                           pagination=posts, total_posts=total_posts, dang_bai=dang_bai, xoa=xoa)

@app.route("/admin", methods=["GET"])
@login_required
def admin():
    if not is_admin_user():
        flash("Bạn không có quyền truy cập trang này.", "danger")
        return redirect(url_for("dashboard"))
    users = User.query.all()
    return render_template("admin.html", users=users)

@app.route("/admin/block_user/<int:user_id>", methods=["POST"])
@login_required
def block_user(user_id):
    if not is_admin_user():
        flash("Bạn không có quyền thực hiện hành động này.", "danger")
        return redirect(url_for("dashboard"))
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash("Không thể khóa tài khoản admin.", "danger")
    else:
        user.is_blocked = not user.is_blocked
        db.session.commit()
        status = "khóa" if user.is_blocked else "mở khóa"
        flash(f"Đã {status} tài khoản {user.username}.", "success")
    return redirect(url_for("admin"))

@app.route("/admin/reset_password/<int:user_id>", methods=["POST"])
@login_required
def reset_password(user_id):
    if not is_admin_user():
        flash("Bạn không có quyền thực hiện hành động này.", "danger")
        return redirect(url_for("dashboard"))
    user = User.query.get_or_404(user_id)
    new_password = "newpassword123"
    user.password = new_password
    db.session.commit()
    flash(f"Đã reset mật khẩu cho {user.username}. Mật khẩu mới: {new_password}", "success")
    return redirect(url_for("admin"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password="1",
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)