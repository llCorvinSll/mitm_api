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

    def test_replace_cfg_if_params_identical(self):
        storage = MockContext("some_random")

        storage.add_mock({
            "command": "foo/bar",
            "params": {"a": 1, "b": "2", "c": False},
            "response": "LOSE",
            "method": "GET",
            "status": 200
        })

        storage.add_mock({
            "command": "foo/bar",
            "params": {"a": 1, "b": "2", "c": False},
            "response": "WIN",
            "method": "GET",
            "status": 200
        })

        self.assertEqual(storage.configs[0]["response"], "WIN")

    def test_not_replace_cfg_if_params_not_identical(self):
        storage = MockContext("some_random")

        storage.add_mock({
            "command": "foo/bar",
            "params": {"a": 1, "b": "2", "c": True},
            "response": "WIN",
            "method": "GET",
            "status": 200
        })

        storage.add_mock({
            "command": "foo/bar",
            "params": {"a": 1, "b": "2", "c": False},
            "response": "LOSE",
            "method": "GET",
            "status": 200
        })

        self.assertEqual(len(storage.configs), 2)
        self.assertEqual(storage.configs[0]["response"], "WIN")
        self.assertEqual(storage.configs[1]["response"], "LOSE")

    def test_add_config(self):
        storage = MockContext("some_random")
        self.assertEqual(len(storage.configs), 0)

        storage.add_mock({
            "command": "foo/bar",
            "params": {"a": 1, "b": "2", "c": False},
            "response": {},
            "method": "GET",
            "status": 200
        })

        self.assertEqual(len(storage.configs), 1)

    def test_add_config_2(self):
        storage = MockContext("some_random")
        self.assertEqual(len(storage.configs), 0)
        storage.add_mock({
            "command": "foo/bar",
            "params": None,
            "response": {"a": "fgdfg", "b": 12, "c": True},
            "method": "GET",
            "status": 200
        })

        self.assertEqual(len(storage.configs), 1)
        self.assertEqual(storage.configs[0]["response"], {"a": "fgdfg", "b": 12, "c": True})

    def test_mobileapi_by_default(self):
        storage = MockContext("some_random")
        storage.add_mock({
            "command": "foo/bar",
            "params": {"a": 1, "b": "2", "c": False},
            "response": {},
            "method": "GET",
            "status": 200
        })

        self.assertEqual(storage.configs[0]["service"], "mobileapi")

    def test_keep_service_field(self):
        storage = MockContext("some_random")
        storage.add_mock({
            "service": "baz",
            "command": "foo/bar",
            "params": {"a": 1, "b": "2", "c": False},
            "response": {},
            "method": "GET",
            "status": 200
        })

        self.assertEqual(storage.configs[0]["service"], "baz")


if __name__ == '__main__':
    unittest.main()
