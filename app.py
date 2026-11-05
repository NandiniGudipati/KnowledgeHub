from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "knowledgehub-development-key"
# --------------------------------
# HOME PAGE
# --------------------------------

@app.route("/")
def home():
    return render_template("index.html")
# --------------------------------
# TEST DATABASE CONNECTION
# --------------------------------

@app.route("/test-db")
def test_db():
    connection = None

    try:
        connection = get_db_connection()

        if connection:
            return "Database connected successfully!"

        return "Database connection failed."

    except Exception as error:
        return f"Database Error: {error}"

    finally:
        if connection and connection.is_connected():
            connection.close()
# --------------------------------
# EMPLOYEE REGISTRATION
# --------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        department = request.form.get("department", "").strip()
        designation = request.form.get("designation", "").strip()

        if not full_name or not email or not password:
            flash("Please fill all required fields.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("register"))

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            hashed_password = generate_password_hash(password)

            cursor.execute(
                """
                INSERT INTO employees
                (full_name, email, password, department, designation)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (full_name, email, hashed_password, department, designation)
            )

            connection.commit()

            flash("Registration successful! Please login.")
            return redirect(url_for("login"))

        except Exception as error:
            if connection:
                connection.rollback()

            print("Registration error:", error)
            flash("Email already exists or registration failed.")

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    return render_template("register.html")
# --------------------------------
# EMPLOYEE LOGIN
# --------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM employees WHERE email = %s",
                (email,)
            )

            employee = cursor.fetchone()

            if employee and check_password_hash(employee["password"], password):

                session["employee_id"] = employee["employee_id"]
                session["employee_name"] = employee["full_name"]

                flash("Login successful!")
                return redirect(url_for("dashboard"))

            flash("Invalid email or password.")

        except Exception as error:
            print("Login error:", error)
            flash("Unable to login. Please try again.")

        finally:
            if cursor:
                cursor.close()

            if connection and connection.is_connected():
                connection.close()

    return render_template("login.html")
# --------------------------------
# DASHBOARD
# --------------------------------

@app.route("/dashboard")
def dashboard():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        employee_name=session["employee_name"]
    )
# --------------------------------
# EMPLOYEE LOGOUT
# --------------------------------

@app.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out successfully.")

    return redirect(url_for("login"))
# --------------------------------
# EMPLOYEE PROFILE
# --------------------------------

@app.route("/profile")
def profile():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM employees
            WHERE employee_id = %s
            """,
            (session["employee_id"],)
        )

        employee = cursor.fetchone()

        return render_template("profile.html", employee=employee)

    except Exception as error:
        print("Profile error:", error)
        return "Unable to load profile."

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
# --------------------------------
# EDIT EMPLOYEE PROFILE
# --------------------------------

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":

            full_name = request.form.get("full_name", "").strip()
            department = request.form.get("department", "").strip()
            designation = request.form.get("designation", "").strip()
            bio = request.form.get("bio", "").strip()
            experience_years = request.form.get("experience_years", 0)

            cursor.execute(
                """
                UPDATE employees
                SET full_name = %s,
                    department = %s,
                    designation = %s,
                    bio = %s,
                    experience_years = %s
                WHERE employee_id = %s
                """,
                (
                    full_name,
                    department,
                    designation,
                    bio,
                    experience_years,
                    session["employee_id"]
                )
            )

            connection.commit()

            session["employee_name"] = full_name

            flash("Profile updated successfully!")
            return redirect(url_for("profile"))

        cursor.execute(
            """
            SELECT *
            FROM employees
            WHERE employee_id = %s
            """,
            (session["employee_id"],)
        )

        employee = cursor.fetchone()

        return render_template("edit_profile.html", employee=employee)

    except Exception as error:
        if connection:
            connection.rollback()

        print("Edit profile error:", error)
        return "Unable to update profile."

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

# --------------------------------
# ADD AND VIEW SKILLS
# --------------------------------

@app.route("/skills", methods=["GET", "POST"])
def skills():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":

            skill_name = request.form.get("skill_name", "").strip()
            proficiency_level = request.form.get("proficiency_level", "").strip()

            if skill_name:

                try:
                    cursor.execute(
                        """
                        INSERT INTO skills
                        (employee_id, skill_name, proficiency_level)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            session["employee_id"],
                            skill_name,
                            proficiency_level
                        )
                    )

                    connection.commit()
                    flash("Skill added successfully!")

                except Exception as insert_error:

                    connection.rollback()

                    if getattr(insert_error, "errno", None) == 1062:
                        flash("This skill already exists in your profile!")
                    else:
                        raise insert_error

            else:
                flash("Please enter a skill name.")

        cursor.execute(
            """
            SELECT *
            FROM skills
            WHERE employee_id = %s
            ORDER BY created_at DESC
            """,
            (session["employee_id"],)
        )

        all_skills = cursor.fetchall()

        return render_template(
            "skills.html",
            all_skills=all_skills
        )

    except Exception as error:

        if connection:
            connection.rollback()

        print("Skills error:", error)
        return "Unable to load skills."

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

# --------------------------------
# ADD AND VIEW PROJECTS
# --------------------------------

@app.route("/projects", methods=["GET", "POST"])
def projects():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":

            project_title = request.form.get("project_title", "").strip()
            project_description = request.form.get("project_description", "").strip()
            technologies_used = request.form.get("technologies_used", "").strip()
            role_in_project = request.form.get("role_in_project", "").strip()
            start_date = request.form.get("start_date") or None
            end_date = request.form.get("end_date") or None

            if project_title:
                cursor.execute(
                    """
                    INSERT INTO projects
                    (
                        employee_id,
                        project_title,
                        project_description,
                        technologies_used,
                        role_in_project,
                        start_date,
                        end_date
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        session["employee_id"],
                        project_title,
                        project_description,
                        technologies_used,
                        role_in_project,
                        start_date,
                        end_date
                    )
                )

                connection.commit()
                flash("Project added successfully!")

        cursor.execute(
            """
            SELECT *
            FROM projects
            WHERE employee_id = %s
            ORDER BY created_at DESC
            """,
            (session["employee_id"],)
        )

        all_projects = cursor.fetchall()

        return render_template(
            "projects.html",
            all_projects=all_projects
        )

    except Exception as error:
        if connection:
            connection.rollback()

        print("Projects error:", error)
        return "Unable to load projects."

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
# --------------------------------
# ADD AND VIEW CERTIFICATIONS
# --------------------------------

@app.route("/certifications", methods=["GET", "POST"])
def certifications():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":

            certification_name = request.form.get("certification_name", "").strip()
            issuing_organization = request.form.get("issuing_organization", "").strip()
            certificate_url = request.form.get("certificate_url", "").strip()

            if certification_name:
                cursor.execute(
                    """
                    INSERT INTO certifications
                    (
                        employee_id,
                        certification_name,
                        issuing_organization,
                        credential_url
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        session["employee_id"],
                        certification_name,
                        issuing_organization,
                        certificate_url
                    )
                )

                connection.commit()
                flash("Certification added successfully!")

        cursor.execute(
            """
            SELECT *
            FROM certifications
            WHERE employee_id = %s
            ORDER BY created_at DESC
            """,
            (session["employee_id"],)
        )

        all_certifications = cursor.fetchall()

        return render_template(
            "certifications.html",
            all_certifications=all_certifications
        )

    except Exception as error:
        if connection:
            connection.rollback()

        print("Certifications error:", error)
        return "Unable to load certifications."

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
# --------------------------------
# KNOWLEDGE ARTICLES
# --------------------------------

@app.route("/articles", methods=["GET", "POST"])
def articles():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":

            topic_name = request.form.get("topic_name", "").strip()
            description = request.form.get("description", "").strip()

            if topic_name and description:

                cursor.execute(
                    """
                    INSERT INTO articles
                    (employee_id, topic_name, description)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        session["employee_id"],
                        topic_name,
                        description
                    )
                )

                connection.commit()
                flash("Knowledge article published successfully!")

        search_query = request.args.get("search", "").strip()

        if search_query:

            cursor.execute(
                """
                SELECT
                    articles.*,
                    employees.full_name,
                    employees.designation
                FROM articles
                JOIN employees
                ON articles.employee_id = employees.employee_id
                WHERE articles.topic_name LIKE %s
                OR articles.description LIKE %s
                ORDER BY articles.created_at DESC
                """,
                (
                    "%" + search_query + "%",
                    "%" + search_query + "%"
                )
            )

        else:

            cursor.execute(
                """
                SELECT
                    articles.*,
                    employees.full_name,
                    employees.designation
                FROM articles
                JOIN employees
                ON articles.employee_id = employees.employee_id
                ORDER BY articles.created_at DESC
                """
            )

        all_articles = cursor.fetchall()

        return render_template(
            "articles.html",
            all_articles=all_articles,
            search_query=search_query
        )

    except Exception as error:
        if connection:
            connection.rollback()

        print("Articles error:", error)
        return "Unable to load knowledge articles."

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()
# --------------------------------
# QUESTIONS AND ANSWERS
# --------------------------------

@app.route("/questions", methods=["GET", "POST"])
def questions():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        if request.method == "POST":

            action = request.form.get("action")

            if action == "ask_question":

                question_title = request.form.get("question_title", "").strip()
                question_description = request.form.get("question_description", "").strip()

                if question_title and question_description:

                    cursor.execute(
                        """
                        INSERT INTO questions
                        (employee_id, question_title, question_description)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            session["employee_id"],
                            question_title,
                            question_description
                        )
                    )

                    connection.commit()
                    flash("Your question has been posted!")

                else:
                    flash("Please enter both question title and description.")

            elif action == "post_answer":

                question_id = request.form.get("question_id")
                answer_description = request.form.get("answer_description", "").strip()

                if question_id and answer_description:

                    cursor.execute(
                        """
                        INSERT INTO answers
                        (question_id, employee_id, answer_description)
                        VALUES (%s, %s, %s)
                        """,
                        (
                            question_id,
                            session["employee_id"],
                            answer_description
                        )
                    )

                    connection.commit()
                    flash("Your answer has been posted!")

                else:
                    flash("Please enter your answer.")

        cursor.execute(
            """
            SELECT
                questions.*,
                employees.full_name,
                employees.designation
            FROM questions
            JOIN employees
            ON questions.employee_id = employees.employee_id
            ORDER BY questions.created_at DESC
            """
        )

        all_questions = cursor.fetchall()

        for question in all_questions:

            cursor.execute(
                """
                SELECT
                    answers.*,
                    employees.full_name,
                    employees.designation
                FROM answers
                JOIN employees
                ON answers.employee_id = employees.employee_id
                WHERE answers.question_id = %s
                ORDER BY answers.created_at ASC
                """,
                (question["question_id"],)
            )

            question["answers"] = cursor.fetchall()

        return render_template(
            "questions.html",
            all_questions=all_questions
        )

    except Exception as error:
        if connection:
            connection.rollback()

        print("Questions error:", error)
        return "Unable to load questions and answers."

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

# --------------------------------
# FIND EMPLOYEE EXPERTS
# --------------------------------

@app.route("/find-experts", methods=["GET"])
def find_experts():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        search_skill = request.args.get("skill", "").strip()
        employees = []

        if search_skill:

            cursor.execute(
                """
                SELECT
                    employees.employee_id,
                    employees.full_name,
                    employees.designation,
                    employees.department,
                    employees.experience_years,

                    GROUP_CONCAT(
                        DISTINCT skills.skill_name
                        SEPARATOR ', '
                    ) AS skills,

                    COUNT(
                        DISTINCT CASE
                            WHEN skills.skill_name LIKE %s
                            THEN skills.skill_id
                        END
                    ) AS match_score

                FROM employees

                JOIN skills
                ON employees.employee_id = skills.employee_id

                GROUP BY
                    employees.employee_id,
                    employees.full_name,
                    employees.designation,
                    employees.department,
                    employees.experience_years

                HAVING match_score > 0

                ORDER BY
                    match_score DESC,
                    employees.experience_years DESC
                """,
                ("%" + search_skill + "%",)
            )

            employees = cursor.fetchall()

        return render_template(
            "find_experts.html",
            employees=employees,
            search_skill=search_skill
        )

    except Exception as error:

        print("Find Experts error:", error)

        return "Unable to search employees."

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

# --------------------------------
# UPVOTE ANSWERS
# --------------------------------

@app.route("/upvote/<int:answer_id>", methods=["POST"])
def upvote_answer(answer_id):

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT IGNORE INTO answer_upvotes
            (answer_id, employee_id)
            VALUES (%s, %s)
            """,
            (answer_id, session["employee_id"])
        )

        connection.commit()

        if cursor.rowcount == 1:
            flash("You upvoted this answer!")
        else:
            flash("You have already upvoted this answer.")

    except Exception as error:
        if connection:
            connection.rollback()

        print("Upvote error:", error)
        flash("Unable to upvote this answer.")

    finally:
        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for("questions"))

# --------------------------------
# MY EXPERTISE PROFILE
# --------------------------------

@app.route("/my-expertise")
def my_expertise():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        employee_id = session["employee_id"]

        # Fetch employee information
        cursor.execute(
            """
            SELECT *
            FROM employees
            WHERE employee_id = %s
            """,
            (employee_id,)
        )

        employee = cursor.fetchone()

        # Fetch employee skills
        cursor.execute(
            """
            SELECT *
            FROM skills
            WHERE employee_id = %s
            ORDER BY created_at DESC
            """,
            (employee_id,)
        )

        all_skills = cursor.fetchall()

        # Fetch employee projects
        cursor.execute(
            """
            SELECT *
            FROM projects
            WHERE employee_id = %s
            ORDER BY created_at DESC
            """,
            (employee_id,)
        )

        all_projects = cursor.fetchall()

        # Fetch employee certifications
        cursor.execute(
            """
            SELECT *
            FROM certifications
            WHERE employee_id = %s
            ORDER BY created_at DESC
            """,
            (employee_id,)
        )

        all_certifications = cursor.fetchall()

        return render_template(
            "my_expertise.html",
            employee=employee,
            all_skills=all_skills,
            all_projects=all_projects,
            all_certifications=all_certifications
        )

    except Exception as error:

        print("My Expertise error:", error)

        return "Unable to load your expertise profile."

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

# --------------------------------
# MY CONTRIBUTIONS
# --------------------------------

@app.route("/my-contributions")
def my_contributions():

    if "employee_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        employee_id = session["employee_id"]

        # Count knowledge articles
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM articles
            WHERE employee_id = %s
            """,
            (employee_id,)
        )
        article_count = cursor.fetchone()["total"]

        # Count questions asked
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM questions
            WHERE employee_id = %s
            """,
            (employee_id,)
        )
        question_count = cursor.fetchone()["total"]

        # Count answers provided
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM answers
            WHERE employee_id = %s
            """,
            (employee_id,)
        )
        answer_count = cursor.fetchone()["total"]

        # Count upvotes received on answers
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM answer_upvotes
            JOIN answers
            ON answer_upvotes.answer_id = answers.answer_id
            WHERE answers.employee_id = %s
            """,
            (employee_id,)
        )
        upvote_count = cursor.fetchone()["total"]

        return render_template(
            "my_contributions.html",
            article_count=article_count,
            question_count=question_count,
            answer_count=answer_count,
            upvote_count=upvote_count
        )

    except Exception as error:

        print("My Contributions error:", error)

        return "Unable to load your contributions."

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()

# --------------------------------
# RUN APPLICATION
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)