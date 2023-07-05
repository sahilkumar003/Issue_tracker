# **Issue Tracker System**

Issue Tracker System is an agile project management tool used by teams to plan, track, release, and support world-class software with confidence. This project is a web-based issue tracking system that allows project teams to effectively track and manage their projects. It provides features to create and track project tasks, assign tasks to team members, and monitor task progress in the form of stories.

## **Features**

- **User Registration**: Users can register on the site by providing their email address, password, first name, last name, date of birth. The system ensures unique and case-insensitive email addresses and enforces password complexity requirements.
- **Authentication**: Registered users can authenticate using their email and password. Once logged in, they are redirected to the dashboard. Guest users can only access the login and signup pages.
- **User Dashboard**: The dashboard displays a list of all projects the user is a member of or owns. The projects can be filtered based on ownership. Clicking on a project title takes the user to the respective story list page.
- **Project Management**: Users can create new projects, edit project settings (such as description and members), and add stories to projects.
- **Story Management**: Users can add, view, update, and delete stories within a project. Stories can be scheduled or unscheduled, assigned to team members, and tracked based on their status (not started, started, finished, delivered). Certain actions have validation rules, such as preventing updates to delivered stories or unscheduling started/finished stories and many more to prevent unconsistency.
- **Profile Management**: Users can view and update their profile information.
- **Email Notifications**: Users receive email notifications for project-related activities, such as being added to a project or being assigned a story and also for greeting for first time registration.

## **Installation**

1. Clone the repository: **`git clone https://github.com/techlyticaly-induction/issue-tracker-sahil.git`**
2. Create a virtual environment: **`python -m venv env`**
3. Activate the virtual environment:
    - For Windows: **`env\Scripts\activate`**
    - For Unix or Linux: **`source env/bin/activate`**
4. Install the project dependencies: **`pip install -r requirements.txt`**
5. Configure the database:
    - Open the **`settings.py`** file in the **`issue_tracker`** directory.
    - Locate the **`DATABASES`** section and update the configuration based on your PostgreSQL settings. Replace the values in angle brackets (**`<>`**) with your actual database credentials.
        
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': '<your_database_name>',
                'USER': '<your_database_user>',
                'PASSWORD': '<your_database_password>',
                'HOST': '<your_database_host>',
                'PORT': '<your_database_port>',
            }
        }
        ```
        
        You can refer to the **[Django documentation](https://docs.djangoproject.com/en/3.2/ref/settings/#databases)** for more information.
        
6. Apply database migrations: **`python manage.py migrate`**
7. To connect the database to PostgreSQL, use the following commands:
    - First, migrate all changes: **`python manage.py migrate`**
    - Create a data dump file (if not already available): **`python manage.py dumpdata > datadump.json`**
    - Load the data from the dump file to the database: **`python manage.py loaddata datadump.json`**
8. Configure email settings:
    - Open the **`settings.py`** file in the **`issue_tracker`** directory.
    - Locate the **`EMAIL_BACKEND`** and **`EMAIL_HOST`** settings and update them according to your email service provider. You can refer to the **[Django documentation](https://docs.djangoproject.com/en/3.2/topics/email/#console-backend)** for examples and additional options. You can also refer to this **[article](https://www.geeksforgeeks.org/setup-sending-email-in-django-project/)** for guidance on setting up email in Django.
9. Start the development server: **`python manage.py runserver`**
10. Access the application in your web browser at **`http://localhost:8000`**

## **Technologies Used**

- Python
- Django
- Django REST Framework
- JavaScript
- HTML
- CSS
- Bootstrap
- PostgreSQL

## **Contributing**

Contributions to Issue Tracker System are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## **License**

This project is licensed under the **Techlyticaly.**
