# from django.test import TestCase
from unittest import mock

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from core.forms import UrlForm
from core.models import Url


# Create your tests here.
class TestUrlModel(TestCase):
    def test_unique_hashed_url_integrity_error(self):
        Url.objects.create(url="https://google.com", hashed_url="test")

        with self.assertRaises(IntegrityError):
            Url.objects.create(url="https://google.com", hashed_url="test")

    def test_automatic_hashes_never_clash(self):
        def _mock_token():
            yield "same"
            yield "same"
            yield "same"
            yield "same"
            yield "different"

        mock_token_generator = _mock_token()

        def mock_token_urlsafe(length: int):
            return str(next(mock_token_generator))

        with mock.patch("secrets.token_urlsafe", mock_token_urlsafe):
            url1 = Url.objects.create(url="https://google.com")
            url2 = Url.objects.create(url="https://opeyadeyemi.com")

        with self.assertRaises(StopIteration):
            next(mock_token_generator)

        self.assertEqual(url1.hashed_url, "same")
        self.assertEqual(url2.hashed_url, "different")


class TestUrlForm(TestCase):
    def test_existing_custom_hash_should_be_invalid(self):
        Url.objects.create(url="https://google.com", hashed_url="test")
        is_valid = UrlForm(data={
            "url": "https://google.com",
            "custom_hash": "test"
        }).is_valid()
        self.assertFalse(is_valid)

    def test_form_without_custom_hash_should_be_valid(self):
        is_valid = UrlForm(data={
            "url": "https://google.com",
            "custom_hash": ""
        }).is_valid()
        self.assertTrue(is_valid)
