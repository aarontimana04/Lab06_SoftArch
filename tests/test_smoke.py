def test_settings_loaded(django_settings):
    assert django_settings.SECRET_KEY, "SECRET_KEY debe estar definido"

def test_math():
    assert 2 + 2 == 4
