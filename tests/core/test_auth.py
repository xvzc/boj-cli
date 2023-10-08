import pytest

import boj.core.auth
from boj.core import auth
from boj.core.data import Credential


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
    k = auth.create_key()
    assert k == expected


@pytest.mark.parametrize(
    "key, plain_text",
    [
        (auth.create_key(), "Hello, world!"),
        (auth.create_key(), "Apple"),
        (auth.create_key(), "Banana"),
        (auth.create_key(), "The quick brown fox jumps over the lazy dog"),
    ],
)
def test_encrypt(key, plain_text):
    c = auth.encrypt(key, plain_text)
    assert c != ""


@pytest.mark.parametrize(
    "key, plain_text",
    [
        (auth.create_key(), "Hello, world!"),
        (auth.create_key(), "Apple"),
        (auth.create_key(), "Banana"),
        (auth.create_key(), "The quick brown fox jumps over the lazy dog"),
    ],
)
def test_decrypt(key, plain_text):
    c = auth.encrypt(key, plain_text)
    p = auth.decrypt(key, c)
    assert p == plain_text


@pytest.mark.parametrize(
    "key, credential",
    [
        (
            auth.create_key(),
            Credential(username="test_user2", token="this-is-test-token1"),
        ),
        (
            auth.create_key(),
            Credential(username="test_user2", token="this-is-test-token2"),
        ),
    ],
)
def test_read_credential(key, credential, mocker):
    def side_effect(path: str, opt):
        if path.endswith("key"):
            return key
        if path.endswith("credential"):
            return boj.core.auth.encrypt(key, credential.to_json())

    mocker.patch("boj.core.util.read_file", side_effect=side_effect)
    credential_result = auth.read_credential()
    assert credential_result == credential
