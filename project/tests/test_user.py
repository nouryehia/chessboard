from project.src.models.user import User

# Constants
first_name = 'Tracker'
last_name = 'Wonderdog'
password = '$pbkdf2-sha256$29000$tLYWAgBAiLGWsvbeuxdijA$mbwptJE6FEUx2MoZM489.F/aYZ9Kn/99hC5DM.jSWG4'

def test_repr():
    user = User()
    user.first_name = first_name
    user.last_name = last_name

    assert repr(user) == f'{first_name} {last_name}'


def test_update_user():
    user = User()

    user.update_user(first_name)

    assert user.first_name == first_name

# Incomplete
def test_reset_password():
    user = User()
    user.email = 'tester@queues.ucsd.edu'

    user.reset_password('password')

    # Requires database connection
    assert User.check_password(user.email, 'password')