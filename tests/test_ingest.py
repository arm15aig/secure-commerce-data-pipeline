import unittest
from unittest.mock import patch, MagicMock
import urllib.error
import sys
import os
import hashlib

# Ensure the test runner can find the 'src' directory across folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from ingest import sanitize_user_records, fetch_raw_user_data


class TestCommerceDataPipeline(unittest.TestCase):

    def setUp(self):
        """Prepares a standardized mock API payload before each test executes."""
        self.mock_raw_payload = [
            {
                "id": 1,
                "username": "johndoe",
                "email": "JohnDoe@Example.com ",  # Intentionally includes uppercase letters and trailing spaces
                "password": "secret_password123", # Crucial: This field must be completely discarded
                "name": {"firstname": "John", "lastname": "Doe"}, # Crucial: This must be completely discarded
                "address": {
                    "city": "Dublin",
                    "zipcode": "D02 X285"
                }
            }
        ]

    def test_gdpr_data_minimization_and_pseudonymization(self):
        """🔒 Scenario 1: Verify raw PII is stripped and emails are securely hashed."""
        sanitized_results = sanitize_user_records(self.mock_raw_payload)
        
        # Ensure we processed exactly one record
        self.assertEqual(len(sanitized_results), 1)
        
        clean_user = sanitized_results[0]
        
        # Verify strict minimization: Sensitive raw fields MUST NOT exist in the output dictionary
        self.assertNotIn("password", clean_user)
        self.assertNotIn("name", clean_user)
        
        # Verify proper lookup structural mapping
        self.assertEqual(clean_user["id"], 1)
        self.assertEqual(clean_user["username"], "johndoe")
        self.assertEqual(clean_user["region"]["city"], "Dublin")
        
        # Verify deterministic one-way SHA-256 encryption logic
        # Expected hash for normalized 'johndoe@example.com'
        normalized_email = "johndoe@example.com"
        expected_hash = hashlib.sha256(normalized_email.encode('utf-8')).hexdigest()
        
        self.assertEqual(clean_user["masked_email"], expected_hash)

    @patch('urllib.request.urlopen')
    def test_fetch_raw_user_data_success(self, mock_urlopen):
        """📡 Scenario 2: Verify successful network extraction returns parsed JSON."""
        # Mock a successful HTTP response string
        mock_response = MagicMock()
        mock_response.read.return_value = b'[{"id": 1, "username": "testuser"}]'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        result = fetch_raw_user_data("https://fake-url.com")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["username"], "testuser")

    @patch('urllib.request.urlopen')
    def test_fetch_raw_user_data_http_error(self, mock_urlopen):
        """❌ Scenario 3: Verify server-side HTTP errors (e.g., 500 Server Error) fail gracefully."""
        # Force urlopen to raise a standard HTTP 500 error
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://fake-url.com",
            code=500,
            msg="Internal Server Error",
            hdrs=None,
            fp=None
        )

        result = fetch_raw_user_data("https://fake-url.com")
        
        # The pipeline must catch the error gracefully and return an empty dataset list rather than crashing
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()