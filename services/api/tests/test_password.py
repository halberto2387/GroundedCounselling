from app.security.password import hash_password, verify_password


def test_password_hash_and_verify():
    plain = "S3cureP@ssw0rd!"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrong", hashed)
