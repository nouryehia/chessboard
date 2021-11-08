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
student_user = User.find_by_pid_email_fallback('', 'student@gmail.com')
tutor_user = User.find_by_pid_email_fallback('', 'tutor@gmail.com')
lead_user = User.find_by_pid_email_fallback('', 'lead@gmail.com')
prof_user = User.find_by_pid_email_fallback('', 'prof@gmail.com')

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

    # Test find by pid
    student_user.pid = '1'
    student_user.save()
    assert User.find_by_pid_email_fallback('1', '') is not None

    # Test find by email
    for email in emails:
        assert User.find_by_pid_email_fallback('', email) is not None

    # Test email fallback
    assert User.find_by_pid_email_fallback('some invalid pid', 'some invalid email') is None
    for email in emails:
        assert User.find_by_pid_email_fallback('some invalid pid', email) is not None


def test_update_login_timestamp():
    user = User()

    old_login = user.last_login
    user.update_login_timestamp()

    assert old_login != user.last_login


def test_generate_token():
    user = User()

    old_token = user.token
    user.generate_token()

    assert old_token != user.token


def test_request_promotion():
    # Test no params
    assert User.request_promotion() == (False, 'missing param', None)

    # Test invalid user id & email
    assert User.request_promotion(-1) == (False, 'user not found', None)
    assert User.request_promotion(None, 'notemail') == (False, 'user not found', None)

    # Test instructor user
    assert User.request_promotion(None, 'lead@gmail.com') == (False, 'already an instructor', lead_user)
    assert User.request_promotion(None, 'prof@gmail.com') == (False, 'already an instructor', prof_user)

    # Test successful request
    assert User.request_promotion(None, 'tutor@gmail.com') == (True, 'success', tutor_user)
    assert tutor_user.request == True

    # Test already requesting check
    assert User.request_promotion(None, 'tutor@gmail.com') == (False, 'already requested', tutor_user)


def test_reset_password():
    student_user.reset_password('new_password')

    assert User.check_password('student@gmail.com', 'new_password')

    # Revert to old password
    student_user.reset_password('password')

