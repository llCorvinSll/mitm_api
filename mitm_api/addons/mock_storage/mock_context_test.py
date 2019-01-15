import unittest

from mitm_api.addons.mock_storage.MockContext import MockContext, get_matched_config


class mock_context_get_mock(unittest.TestCase):
    def __init__(self, m_name):
        super().__init__(m_name)

        self.context = None

    def setUp(self):
        self.context = MockContext("")

    def test_mock_without_url_params(self):
        configs = [
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "bar",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/baz",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "baz",
                "method": "GET",
                "status": 200
            }
        ]

        self.assertIsNone(get_matched_config("mobileapi", "GET", "foo/bar", {}, configs))

    def test_mock_without_url_params_and_matched_config(self):
        configs = [
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {},
                "response": "win",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "lose",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/baz",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "baz",
                "method": "GET",
                "status": 200
            }
        ]

        self.assertEqual(get_matched_config("mobileapi", "GET", "foo/bar", {}, configs),
                         {"response": "win", "status": 200})

    def test_mock_without_url_params_and_matched_config_2(self):
        configs = [
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {},
                "response": "win",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "lose",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/baz",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "baz",
                "method": "GET",
                "status": 200
            }
        ]

        self.assertEqual(get_matched_config("mobileapi", "GET", "foo/bar", {"a": 1}, configs),
                         {"response": "lose", "status": 200})

    def test_mock_without_url_params_and_matched_config_3(self):
        configs = [
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {},
                "response": "win",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "lose",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/baz",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "baz",
                "method": "GET",
                "status": 200
            }
        ]

        self.assertEqual(get_matched_config("mobileapi", "GET", "foo/bar", {"a": 4}, configs),
                         {"response": "lose", "status": 200})

    def test_mock_with_params(self):
        #         test("ищет совпадения по url при совпадении параметров", () => {
        configs = [
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "bar",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/baz",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "baz",
                "method": "GET",
                "status": 200
            }
        ]

        self.assertEqual(get_matched_config("mobileapi", "GET", "foo/bar", {"a": 1, "b": "2", "c": False}, configs),
                         {"response": "bar", "status": 200})

    def test_format_url_by_standard(self):
        configs = [
            {
                "service": "mobileapi",
                "command": "foo/bar/",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "bar",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/baz",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "baz",
                "method": "GET",
                "status": 200
            }
        ]

        self.assertEqual(get_matched_config("mobileapi", "GET", "foo/bar", {"a": 1, "b": "2", "c": False}, configs),
                         {"response": "bar", "status": 200})

    def test_match_mock_by_parameters(self):
        #         test("находит наиболее подходящий по количеству параметров запрос", () => {
        configs = [
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {"a": 1, "b": "2"},
                "response": "baz",
                "method": "GET",
                "status": 200
            },
            {
                "service": "mobileapi",
                "command": "foo/bar",
                "params": {"a": 1, "b": "2", "c": False},
                "response": "bar",
                "method": "GET",
                "status": 200
            }
        ];
        #
        self.assertEqual(get_matched_config("mobileapi", "GET", "foo/bar", {"a": 1, "b": "2", "c": False, "d": "tttt"},
                                            configs), {"response": "bar", "status": 200})


if __name__ == '__main__':
    unittest.main()
