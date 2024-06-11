# app.py
from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
from forms import LoginForm, PostForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'saim2024@stella'

# Function to create a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('site.db')
    conn.row_factory = sqlite3.Row
    return conn

# Check if user is logged in
def is_logged_in():
    return 'user_id' in session

# Route to handle creating a new post
@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if not is_logged_in():
        return redirect(url_for('login'))  # Redirect to login if not logged in
    form = PostForm()
    if form.validate_on_submit():
        author_name = request.form.get('author')  # Get author name from the form
        category = form.category.data
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content, author, category) VALUES (?, ?, ?, ?)',
                     (form.title.data, form.content.data, author_name, category))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add_post.html', form=form)

# Route to handle editing a post
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    if not is_logged_in():
        return redirect(url_for('login'))  # Redirect to login if not logged in
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    form = PostForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (form.title.data, form.content.data, post_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post['title']
        form.content.data = post['content']
    return render_template('edit_post.html', form=form)

# Route to handle deleting a post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    if not is_logged_in():
        return redirect(url_for('login'))  # Redirect to login if not logged in
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# Route to display all posts for editing or deleting
@app.route('/posts')
def list_posts():
    if not is_logged_in():
        return redirect(url_for('login'))  # Redirect to login if not logged in
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('list_posts.html', posts=posts)



@app.route('/category/<string:category>')
def category_posts(category):
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts WHERE category = ?', (category,)).fetchall()  
    conn.close()
    return render_template('category_posts.html', posts=posts, category=category)


...



# # Route to display posts
# @app.route('/')
# def home():
#     conn = get_db_connection()
#     posts = conn.execute('SELECT * FROM posts').fetchall()
#     conn.close()
#     return render_template('home.html', posts=posts)


@app.route('/', methods=['GET'])
def home():
    conn = get_db_connection()
    search_query = request.args.get('q')
    per_page = 12  # Number of posts per page

    if search_query:
        query = f"SELECT COUNT(*) FROM posts WHERE title LIKE '%{search_query}%' OR content LIKE '%{search_query}%'"
        total_posts = conn.execute(query).fetchone()[0]  # Total number of posts matching the search query
        total_pages = (total_posts + per_page - 1) // per_page  # Calculate total pages for pagination

        page = request.args.get('page', 1, type=int)  # Get the page number from the request parameters, default to 1
        offset = (page - 1) * per_page  # Calculate the OFFSET for pagination

        query = f"SELECT * FROM posts WHERE title LIKE '%{search_query}%' OR content LIKE '%{search_query}%' ORDER BY id DESC LIMIT ? OFFSET ?"
        posts = conn.execute(query, (per_page, offset)).fetchall()
        conn.close()

        return render_template('search.html', posts=posts, query=search_query, page=page, total_pages=total_pages)
    else:
        query = 'SELECT COUNT(*) FROM posts'
        total_posts = conn.execute(query).fetchone()[0]  # Total number of posts
        total_pages = (total_posts + per_page - 1) // per_page  # Calculate total pages for pagination

        page = request.args.get('page', 1, type=int)  # Get the page number from the request parameters, default to 1
        offset = (page - 1) * per_page  # Calculate the OFFSET for pagination

        posts = conn.execute('SELECT * FROM posts ORDER BY id DESC LIMIT ? OFFSET ?', (per_page, offset)).fetchall()
        conn.close()

        return render_template('home.html', posts=posts, page=page, total_pages=total_pages)




# Route to display about page
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)', (name, email, message))
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))  # Redirect to home after submitting the form
    
    return render_template('contact.html')

# Route to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (form.username.data, form.password.data)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

# Route to handle user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


# Route to display a single post
@app.route('/post/<int:post_id>')
def post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
