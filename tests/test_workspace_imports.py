import unittest

import api_service
import bot_service


class WorkspaceImportsTest(unittest.TestCase):
    def test_api_service_package_is_importable(self) -> None:
        self.assertEqual(api_service.__version__, "0.1.0")

    def test_bot_service_package_is_importable(self) -> None:
        self.assertEqual(bot_service.__version__, "0.1.0")


if __name__ == "__main__":
    unittest.main()
