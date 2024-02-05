import pytest

from boj.core import crypto


@pytest.mark.parametrize(
    "key, plain_text",
    [
        (crypto.create_key(), "Hello, world!"),
        (crypto.create_key(), "Apple"),
        (crypto.create_key(), "Banana"),
        (crypto.create_key(), "The quick brown fox jumps over the lazy dog"),
    ],
)
def test_decrypt(key, plain_text):
    c = crypto.encrypt(key, plain_text.encode("utf-8"))
    p = crypto.decrypt(key, c)
    assert p == bytes(plain_text, "utf-8")
