from app.models import UserModel


def test_new_user(new_user):
    assert new_user.email == "tester77@gmail.com"
    assert new_user.password != "strong_password"
    assert new_user.__repr__() == "<User: tester77@gmail.com>"


def test_setting_password(new_user):
    new_user.set_password("MyNewPassword")
    assert new_user.password != "MyNewPassword"
    assert new_user.is_password_correct("MyNewPassword")
    assert not new_user.is_password_correct("MyNewPassword2")
    assert not new_user.is_password_correct("strong_password")
