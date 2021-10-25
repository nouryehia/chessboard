from project.src.models.user import User

# Constants
first_name = 'Tracker'
last_name = 'Wonderdog'
emails = [
    'student@gmail.com',
    'tutor@gmail.com',
    'lead@gmail.com',
    'prof@gmail.com'
]
password = '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4'


# Tests
## Methods used in the controller
def test_update_user():
    user = User()

    user.update_user(first_name)

    assert user.first_name == first_name


def test_check_password():
    for email in emails:
        assert User.check_password(email, 'password')


def test_find_by_email_fallback():
    # Test empty pid check
    assert User.find_by_pid_email_fallback('', '') is None
    for email in emails:
        assert User.find_by_pid_email_fallback('', email) is not None

    # Test email fallback
    assert User.find_by_pid_email_fallback('some invalid pid', 'some invalid email') is None
    for email in emails:
        assert User.find_by_pid_email_fallback('some invalid pid', email) is not None


def test_reset_password():
    user = User()
    user.email = 'student@gmail.com'

    user.reset_password('password')

    # Requires database connection
    assert User.check_password(user.email, 'password')
