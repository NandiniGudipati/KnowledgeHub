# KnowledgeHub – Employee Knowledge Sharing & Expertise Discovery Platform

**CONNECT • SHARE • GROW**

KnowledgeHub is an employee-focused knowledge-sharing platform designed to encourage collaboration and make organizational knowledge easily accessible in one place.

The platform allows employees to build professional profiles, showcase their skills, projects and certifications, share technical knowledge, ask questions, provide answers and discover colleagues based on their expertise.

## 🎯 Project Objective

The main objective of KnowledgeHub is to create a centralized platform where employees can:

- Share technical knowledge and ideas.
- Discover employees with relevant skills and expertise.
- Showcase their professional experience and achievements.
- Ask questions and learn from other employees.
- Encourage collaboration and knowledge sharing within an organization.

## ✨ Features

### 1. Employee Registration & Login
- Employee registration and authentication.
- Secure password hashing.
- Session-based login management.

### 2. Employee Profile Management
- View and update employee information.
- Maintain department, designation, bio and experience details.

### 3. Skills Management
- Add technical skills.
- Specify proficiency levels.
- Prevent duplicate skill entries.

### 4. Project Management
- Add and maintain project details.
- View previously added projects.
- Prevent duplicate project entries.

### 5. Certifications Management
- Add professional certifications.
- Maintain certification and issuing organization details.
- Prevent duplicate certification entries.

### 6. Knowledge Articles
- Publish technical knowledge articles.
- Browse articles shared by employees.
- Search articles using topic names and descriptions.

### 7. Find Experts
- Search employees based on technical skills.
- Identify employees with matching expertise.
- Rank matching employees using skill matches and experience.

### 8. Questions & Answers
- Ask technical questions.
- Post answers to questions.
- View answers shared by employees.
- Upvote useful answers.
- View upvote information.

### 9. My Expertise
- View professional skills.
- Showcase projects and certifications.
- Maintain an overview of employee expertise.

### 10. My Contributions
- Track knowledge articles published.
- Count questions asked and answers posted.
- View upvotes received on answers.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap | Responsive user interface |
| JavaScript | Frontend interactions |
| MySQL | Relational database |
| mysql-connector-python | Python–MySQL connectivity |
| Werkzeug | Password hashing |
| Aiven | Cloud database hosting |
| GitHub | Version control and source code management |
| Vercel | Application deployment |

## 🗄️ Database Structure

KnowledgeHub uses MySQL with the following main tables:

| Table | Description |
|---|---|
| `employees` | Stores employee account and profile details |
| `skills` | Stores employee skills and proficiency levels |
| `projects` | Stores employee project information |
| `certifications` | Stores professional certifications |
| `articles` | Stores knowledge-sharing articles |
| `questions` | Stores employee questions |
| `answers` | Stores answers posted by employees |
| `answer_upvotes` | Stores employee upvotes on answers |

The database uses relationships between employee records and their associated skills, projects, certifications, articles, questions and answers.

## 📂 Project Structure

```text
KnowledgeHub/
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── edit_profile.html
│   ├── skills.html
│   ├── projects.html
│   ├── certifications.html
│   ├── articles.html
│   ├── questions.html
│   ├── find_experts.html
│   ├── my_expertise.html
│   └── my_contributions.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── knowledgehub_logo.png
│
└── README.md
```

## ⚙️ Installation & Setup

Follow these steps to run KnowledgeHub locally.

### 1. Clone the Repository

```bash
git clone https://github.com/NandiniGudipati/KnowledgeHub.git
```

### 2. Navigate to the Project Directory

```bash
cd KnowledgeHub
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux / macOS:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Database

- Install and configure MySQL.
- Create a database named `knowledgehub`.
- Create the required tables.
- Configure database credentials in your configuration file.
- Ensure the database connection settings are correct.

Keep database passwords and secret keys in environment variables. Do not commit sensitive credentials to GitHub.

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## ☁️ Deployment

The application is deployed using:

- **GitHub:** Source code repository.
- **Aiven:** Cloud-hosted MySQL database.
- **Vercel:** Web application hosting.

## 🔐 Security & Data Management

- Passwords are stored as secure hashes rather than plain text.
- Flask sessions are used to manage authenticated employees.
- Parameterized SQL queries are used for database operations.
- Database transactions use commit and rollback operations.
- Duplicate entries are prevented through application-level checks and database constraints.

## 🚀 Future Enhancements

Potential improvements include:

- Advanced knowledge article categorization and tagging.
- Improved search ranking.
- Expertise scoring and employee recommendations.
- Enhanced contribution analytics.
- Notifications for questions and answers.
- More advanced employee collaboration features.

## 👩‍💻 Project Information

**Project Name:** KnowledgeHub

**Project Type:** Employee Knowledge Sharing & Expertise Discovery Platform

**Developer:** Nandini

**GitHub Repository:** https://github.com/NandiniGudipati/KnowledgeHub

**Live Application:** https://knowledge-hub-two-pied.vercel.app/

---

### CONNECT • SHARE • GROW

*KnowledgeHub – Bringing employee knowledge and expertise together in one place.*
