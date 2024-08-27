# Django-Authentication

Django-Authentication is a Django application designed to centralize all the options and needs related to account authentication and authorization. It offers two deployment options:

1. **With Templates:** Commented code to serve views using HTML templates from the Django server.
2. **As an API:** Using the Django REST Framework to serve a full API for user management.

## Application Structure

The application is organized into several key modules:

- **templates/**: Contains all the HTML for the template-based views.
- **admin/**: Configures the display and management of models in the Django admin panel.
- **forms/**: Forms to be used with HTML templates.
- **models/**: Defines the data models, including `User`, `Group`, and `OneTimePassword`.
- **permissions/**: Permission classes for the API views, checking for authentication permissions.
- **serializers/**: Serializers used in the API views to convert complex data to native data types.
- **tests/**: Includes tests for both the template-based views and the core API functions.
- **urls/**: Contains two `urlpatterns`, one commented for the template-based views and one for the core API.
- **utils/**: General functions and utilities used throughout the application.
- **views/**: Defines all views, both for templates and for the API.

## Main Models

### `User`
The `User` model inherits from `AbstractBaseUser` and `PermissionsMixin`, and uses a custom `UserManager` to handle the creation of users, staff users, and superusers. This model uses email as the primary authentication field (`USERNAME_FIELD`).

### `Group`
An extension of Django's `Group` model, adding a `description` field.

### `OneTimePassword`
Model for managing one-time passwords, associated with each `User`.

## Main Views

### API Based Views

- **UserRegisterView:** Register new users and send verification email.
- **VerifyEmail:** Verify email address.
- **UserLoginView:** Login users.
- **UserProfileView:** View user profile.
- **UserChangePasswordView:** Change password.
- **UserPasswordResetView:** Reset password.
- **UserLogoutView:** Logout.
- **UserDeleteView:** Deletion of user accounts.
- **UserUpdateView:** Update user profile.

### Template-Based Views

The code for these views is commented out but available if you choose to serve views from the Django server using HTML templates.

## Installation

1. Clone this repository.
2. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```
3. Perform the database migrations:
```bash
python manage.py migrate
```
4. Create a superuser:
```bash
python manage.py createsuperuser
```
5. Run the server:
```bash
python manage.py runserver
```

## Usage

You can use this application either as a standalone API or integrate it into a larger project. Setting the URLs allows you to switch between template views and API views depending on your needs.

## Tests

To run the tests, use:
```bash
python manage.py test
```
