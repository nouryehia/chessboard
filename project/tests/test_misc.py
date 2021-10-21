from src.utils.pass_gen import gen_password


def test_pass_gen():
    assert gen_password(10) != gen_password(10)

def test_pass_gen2():
    assert gen_password(5) != gen_password(5)