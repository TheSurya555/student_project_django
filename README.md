# Student Project Django

This repository contains a Django implementation for managing various aspects of a student-related project. The application includes user profiles, blog posts, services, and more.

## Features

- **User Management**: Custom user profiles for different roles (Recruiter, Candidate, Admin).
- **Blog System**: Create, view, and manage blog posts with TinyMCE editor integration.
- **Services**: List and manage services related to student projects.
- **Pagination**: Efficient handling of large datasets with pagination.
- **User Status**: Display online status of users.
- **Profile Management**: Handle user profile images and preferences.

## Requirements

- Python 3.x
- Django 3.x or later
- SQLite (default) or any other database backend supported by Django
- TinyMCE

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/TheSurya555/student_project_django.git
    cd student_project_django
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the application:**

    Open your browser and navigate to `http://127.0.0.1:8000`.

## Usage

- **Home Page**: Displays services, user profiles, and blog posts.
- **Profile Management**: Users can update their profile details, including profile images.
- **Blog System**: Create and manage blog posts with the integrated TinyMCE editor.
- **User Status**: View the online status of users.

## File Structure

- `signUp/models.py`: Contains models for CustomUser, RecruiterProfile, CandidateProfile, and AdminProfile.
- `views.py`: Handles rendering templates, user authentication, and context data.
- `templates/`: Contains HTML templates for rendering views.
- `static/`: Contains static files (CSS, JS, images).

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [TinyMCE](https://www.tiny.cloud/)
