import pytest

import boj.core.crypto
from boj.core import crypto
from boj.data.credential import Credential


@pytest.mark.parametrize(
    "expected",
    [
        "this-is-test-key1",
        "sample-key1",
        "sample-key3",
    ],
)
def test_create_key(expected, mocker):
    mocker.patch("cryptography.fernet.Fernet.generate_key", return_value=expected)
    k = crypto.create_key()
    assert k == expected


@pytest.mark.parametrize(
    "key, plain_text",
    [
        (crypto.create_key(), "Hello, world!"),
        (crypto.create_key(), "Apple"),
        (crypto.create_key(), "Banana"),
        (crypto.create_key(), "The quick brown fox jumps over the lazy dog"),
    ],
)
def test_encrypt(key, plain_text):
    c = crypto.encrypt(key, plain_text)
    assert c != ""


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
    c = crypto.encrypt(key, plain_text)
    p = crypto.decrypt(key, c)
    assert p == plain_text
