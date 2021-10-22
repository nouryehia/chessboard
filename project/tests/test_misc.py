from project.src.utils.pass_gen import gen_password


def test_pass_gen():
    assert gen_password(10) != gen_password(10)
