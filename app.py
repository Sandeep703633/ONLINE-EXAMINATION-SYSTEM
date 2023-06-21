from flask_mysqldb import MySQL
from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_session import Session
import datetime
from flask_login import current_user

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sandeep'
app.config['MYSQL_DB'] = 'E_xam'
app.config['SECRET_KEY'] = 'E_xam'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
mysql = MySQL(app)

# Define a route for the title page
@app.route('/')
def index():
    return render_template('title.html')

# Define a route for the admin page
@app.route('/admin')
def admin(): # Example: setting username in session
    return render_template('admin/admin.html')

@app.route('/user')
def user(): # Example: setting username in session
    return render_template('users/user.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if session.get('admin'): 
    # Example: checking username in session
        return render_template('admin/dashboard.html')
    else:
        return redirect(url_for('index'))

# Define a route for the admin-signup page
@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM admin")
    admin_count = cur.fetchone()[0]
    cur.close()

    if admin_count >= 1:
        return "Permission Not Granted"

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO admin (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()
        cur.close()

        flash("Admin sign-up successful")

    return render_template('admin/admin_signup.html')

# Define a route for the admin-login page
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
        admin = cur.fetchone()
        cur.close()

        if admin:
            # Perform admin login logic
            session['admin'] = email
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials")

    return render_template('admin/admin_login.html')

# Define a route for the user-signup page
@app.route('/user/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()
        cur.close()

        return "User sign-up successful"

    return render_template('users/user_signup.html')

# Define a route for the user-login page
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Perform user login logic
            cur = mysql.connection.cursor()
            cur.execute("SELECT id from users WHERE email=%s",[email])
            id1=cur.fetchone()[0]
            session['user'] = id1
            return render_template('users/dashboard.html')
        else:
            return "Invalid credentials"

    return render_template('users/user_login.html')

# Define a route for the user-logout page
@app.route('/user/logout')
def user_logout():
    session.pop('user')
    return redirect(url_for('index'))

# Define a route for the admin-logout page
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin')
    return redirect(url_for('index'))

# Define a route for the inside admin-login create-exam page


# Define a route for the create-exam page
@app.route('/create-exam', methods=['GET', 'POST'])
def create_exam():
    if 'admin' not in session:  # Check if the user is logged in
        return redirect(url_for('index'))

    if request.method == 'POST':
        subject_code = request.form.get('subjectCode')
        exam_name = request.form.get('examName')
        exam_date = request.form.get('examDate')
        time_limit = request.form.get('timeLimit')
        total_marks = request.form.get('totalMarks')

        if not subject_code or not exam_name or not exam_date or not time_limit or not total_marks:
            flash('Please fill in all the fields')
            return render_template('admin/create_exam.html')

        try:
            time_limit = datetime.datetime.strptime(time_limit, '%H:%M').time()
        except ValueError:
            flash('Invalid time format for time limit. Please use HH:MM format.')
            return render_template('admin/create_exam.html')

        cur = mysql.connection.cursor()
        cur.execute('SELECT subject_code FROM c_exam WHERE subject_code = %s', (subject_code,))
        data = cur.fetchone()
        cur.close()

        if data:
            flash('Subject code already exists')
            return render_template('admin/create_exam.html')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO c_exam (subject_code, exam_name, exam_date, time_limit, total_marks) VALUES (%s, %s, %s, %s, %s)",
                    (subject_code, exam_name, exam_date, time_limit, total_marks))
        mysql.connection.commit()
        cur.close()

        flash('Exam created successfully')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/create_exam.html')



# Define a route for the create-question page
@app.route('/create-question/<subject_code>', methods=['GET', 'POST'])
def create_question(subject_code):
    if 'admin' not in session:  # Check if the user is logged in
        return redirect(url_for('index'))

    if request.method == 'POST':
        question_body = request.form.get('questionBody')
        option_1 = request.form.get('option1')
        option_2 = request.form.get('option2')
        option_3 = request.form.get('option3')
        option_4 = request.form.get('option4')
        correct_option = request.form.get('correctOption')
        marks = request.form.get('marks')

        if not question_body or not option_1 or not option_2 or not option_3 or not option_4 or not correct_option or not marks:
            flash('Please fill in all the fields')
            return render_template('admin/create_question.html', subject_code=subject_code)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO start_exam (body, option_1, option_2, option_3, option_4, correct_option, sub_id, marks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (question_body, option_1, option_2, option_3, option_4, correct_option, subject_code, marks))
        mysql.connection.commit()
        cur.close()

        flash('Question created successfully')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/create_question.html', subject_code=subject_code)


@app.route('/exams-list', methods=['GET', 'POST'])
def exams_list():
    if 'admin' not in session:  # Check if the user is logged in
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT subject_code, exam_name FROM c_exam ORDER BY exam_date DESC')
    data = cur.fetchall()
    cur.close()

    return render_template('admin/exams_list.html', data=data)


@app.route('/modify-list', methods=['GET', 'POST'])
def modify_list():
    if 'admin' not in session:  # Check if the user is logged in
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT subject_code, exam_name FROM c_exam ORDER BY exam_date DESC')
    data = cur.fetchall()
    cur.close()

    return render_template('admin/modify_list.html', data=data)


@app.route('/modify-questions/<subject_code>', methods=['GET', 'POST'])
def modify_questions(subject_code):
    if 'admin' not in session:  # Check if the user is logged in
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        question_id = request.form.get('questionId')
        question_body = request.form.get('questionBody')
        option_1 = request.form.get('option1')
        option_2 = request.form.get('option2')
        option_3 = request.form.get('option3')
        option_4 = request.form.get('option4')
        correct_option = request.form.get('correctOption')
        marks = request.form.get('marks')

        cur = mysql.connection.cursor()
        cur.execute("UPDATE start_exam SET body=%s, option_1=%s, option_2=%s, option_3=%s, option_4=%s, correct_option=%s, marks=%s WHERE id=%s AND sub_id=%s",
                    (question_body, option_1, option_2, option_3, option_4, correct_option, marks, question_id, subject_code))
        mysql.connection.commit()
        cur.close()

        flash('Question modified successfully')
        return redirect(url_for('admin_dashboard'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM start_exam WHERE sub_id=%s", (subject_code,))
    questions = cur.fetchall()
    cur.close()

    return render_template('admin/modify_questions.html', subject_code=subject_code, questions=questions)



@app.route('/delete-exam', methods=['GET', 'POST'])
def delete_exam():
    if 'admin' not in session:  # Check if the user is logged in
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        subject_code = request.form['examId']

        # Check if the subject code exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT subject_code FROM c_exam WHERE subject_code = %s", (subject_code,))
        data = cur.fetchone()
        cur.close()

        if not data:
            flash('Subject code does not exist')
            return render_template('admin/delete_exam.html')

        # Perform the deletion operation using the subject_code
        cur = mysql.connection.cursor()

        # Delete associated records from exam_results table
        # cur.execute("DELETE FROM exam_results WHERE subject_code = %s", (subject_code,))

        # Delete from c_exam table
        cur.execute("DELETE FROM c_exam WHERE subject_code = %s", (subject_code,))

        mysql.connection.commit()
        cur.close()

        flash('Exam deleted successfully')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/delete_exam.html')


# # Define a route for the inside admin-login view-results page
# @app.route('/view-results')
# def view_results():
#     if 'admin' not in session:  # Check if the user is logged in
#         return redirect(url_for('admin_login'))

#     return render_template('admin/view_results.html')


# Define a route for the admin to view all exam results
@app.route('/view-results')
def view_results():
    if 'admin' not in session:  # Check if the user is logged in
        return redirect(url_for('admin_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT subject_code, total_score, INCORRECT, attempted_by FROM exam_results")
    view_results = cur.fetchone()
    cur.close()

    return render_template('admin/view_results.html', results=view_results)



# Define a route for the inside user-login page
@app.route('/view-list')
def view_list():
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('user_login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT subject_code, exam_name, time_limit, total_marks FROM c_exam ORDER BY exam_date DESC')
    data = cur.fetchall()
    cur.close()

    return render_template('users/view_list.html', data=data)


@app.route('/exam-list')
def exam_list():
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('user_login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT subject_code, exam_name FROM c_exam ORDER BY exam_date DESC')
    data = cur.fetchall()
    cur.close()

    return render_template('users/exams_list.html', data=data)


@app.route('/instruction/<subject_code>')
def instructions(subject_code):
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('user_login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT exam_name, exam_date, time_limit, total_marks FROM c_exam WHERE subject_code = %s', (subject_code,))
    data = cur.fetchone()
    cur.close()

    if not data:
        flash('Invalid subject code')
        return redirect(url_for('home'))

    exam_name = data[0]
    exam_date = data[1]
    time_limit = data[2]
    total_marks = data[3]

    return render_template('users/instructions.html', subject_code=subject_code, exam_name=exam_name, exam_date=exam_date, time_limit=time_limit, total_marks=total_marks)



@app.route('/start-exam/<subject_code>')
def start_exam(subject_code):
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('user_login'))

    cur = mysql.connection.cursor()
    cur.execute('SELECT id, body, option_1, option_2, option_3, option_4 FROM start_exam WHERE sub_id = %s', (subject_code,))
    questions = cur.fetchall()
    cur.close()

    return render_template('users/start_exam.html', subject_code=subject_code, questions=questions)


@app.route('/allquestions')
def allquestions():
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('admin_login'))

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, body, sub_id FROM start_exam')
    data = cursor.fetchall()
    cursor.close()

    return render_template('admin/allquestions.html', data=data)


@app.route('/updatequestion/<int:question_id>', methods=['GET', 'POST'])
def updatequestion(question_id):
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        # Update the question in the database based on the form data
        updated_body = request.form['questionBody']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correctOption']
        marks = request.form['marks']

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE start_exam SET body = %s, option_1 = %s,  option_2= %s, option_3 = %s, option_4 = %s, correct_option = %s ,marks=%s WHERE id = %s',
                       (updated_body, option1, option2, option3, option4, correct_option, marks, question_id))
        mysql.connection.commit()
        cursor.close()

        flash('Question updated successfully')
        return redirect('/allquestions')

    # Fetch the existing question data from the database
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM start_exam WHERE id = %s', (question_id,))
    question = cursor.fetchone()
    cursor.close()

    return render_template('admin/modify_exam.html', question=question)


@app.route('/deletequestion/<int:question_id>')
def deletequestion(question_id):
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('admin_login'))

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM start_exam WHERE id = %s', (question_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Question deleted successfully')
    return redirect(url_for('allquestions'))

@app.route('/view-attempted-exams')
def view_attempted_exams():
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('user_login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT  c.exam_name, c.subject_code,e.total_score,e.INCORRECT FROM c_exam c INNER JOIN exam_results e ON c.subject_code = e.subject_code and e.attempted_by=%s",[session.get('user')])
    attempted_exams = cur.fetchall()
    cur.close()

    return render_template('users/view_attempted_exams.html', attempted_exams=attempted_exams)





@app.route('/view-result')
def view_result():
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('user_login'))

    return render_template('users/view_result.html')


@app.route('/submit-exam/<subject_code>', methods=['POST'])
def submit_exam(subject_code):
    if 'user' not in session:  # Check if the user is logged in
        return redirect(url_for('user_login'))

    try:
        # Get the submitted answers from the form data
        submitted_answers = {}
        for question_id, answer in request.form.items():
            if question_id.startswith('answer'):
                question_id = question_id[6:]
                submitted_answers[int(question_id)] = answer

        # Retrieve the correct answers and marks from the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, correct_option, marks FROM start_exam WHERE sub_id = %s", (subject_code,))
        questions = cur.fetchall()
        cur.close()

        # Calculate the total score and mark each question
        total_score = 0
        marked_questions = []
        for question in questions:
            question_id = question[0]
            correct_option = question[1]
            marks = question[2]

            # Check if the submitted answer matches the correct option
            if question_id in submitted_answers and submitted_answers[question_id] == correct_option:
                total_score += marks
                marked_questions.append((question_id, True))
            else:
                marked_questions.append((question_id, False))

        # Store the result in the exam_results table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO exam_results (subject_code, total_score, attempted_by) VALUES (%s, %s, %s)",
                    (subject_code, total_score, session['user']))  # Replace 'user' with the key used to store the user ID in the session
        cur.close()
        mysql.connection.commit()

        # Display the result to the user
        return render_template('users/result.html', total_score=total_score, marked_questions=marked_questions)

    except Exception as e:
        print(e)
        # Handle any exceptions that occur during the submission process
        flash('An error occurred during submission: {}'.format(str(e)))
        return redirect(url_for('index'))

@app.route('/admin-view-attempted-exams')
def admin_view_attempted_exams():
    # Uncomment authentication and authorization code if desired

    cur = mysql.connection.cursor()
    cur.execute("SELECT u.email, c.exam_name, c.subject_code, e.total_score, e.INCORRECT FROM c_exam c INNER JOIN exam_results e ON c.subject_code = e.subject_code INNER JOIN users u ON e.attempted_by = u.id")
    attempted_exams = cur.fetchall()
    cur.close()

    return render_template('admin/view_attempted_exams.html', attempted_exams=attempted_exams)





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


#THE END THEAM ONLINE-EXAMINATION-SYSTEM