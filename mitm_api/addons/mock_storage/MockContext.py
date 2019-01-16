import json

from mitmproxy import http, ctx


class MockContext:
    def __init__(self, key: str):
        self.configs = []
        self.key = key
        self.redirects = {}

    def add_redirect(self, from_url, to_url):
        self.redirects[from_url] = to_url

    def get_redirect(self, url):
        if url in self.redirects.keys():
            return self.redirects[url]

    def add_mock(self, config):

        if "service" not in config:
            config["service"] = "mobileapi"

        if "status" not in config:
            config["status"] = 200

        self.configs.append(config)

    def get_mock(self, flow: http.HTTPFlow):
        service = flow.request.path.split('/')[1]

        raw_url = flow.request.path.split('?')[0]

        raw_url = raw_url.split('/')

        raw_url.pop(0)
        raw_url.pop(0)

        method = '/'.join(map(str, raw_url))

        print(service, method, flow.request.method)

        print(flow.request.query)

        params = {}

        for key in flow.request.query:
            params[key] = flow.request.query[key]

        for key in flow.request.urlencoded_form:
            params[key] = flow.request.urlencoded_form[key]

        mock = get_matched_config(service, flow.request.method, method, params, self.configs)

        if mock:
            ctx.log("[mocking][{}] {}".format(self.key, method))
            flow.response.text = json.dumps(mock["response"]["result"])
            flow.response.status_code = mock["status"]


def get_matched_config(service, method, command, params, configs):
    pre_results = []

    for value in configs:
        if not (value["service"] and value["service"] == service):
            continue

        if value["method"] != method:
            continue

        norm_command = normalise_path(command)
        norm_value_command = normalise_path(value["command"])

        if norm_command == norm_value_command:
            pre_results.append(value)

    if len(params.keys()) == 0:
        empty_results = list(filter(lambda cfg: not "params" in cfg or len(cfg["params"]) == 0, pre_results))

        if len(empty_results):
            return format_response(empty_results[0])

        return None

    max_intersection_weight = 0
    result = None

    for value in pre_results:
        intersection_weight = 0

        if "params" in value:

            mock_params = value["params"]

            for i in mock_params.keys():
                if i in mock_params and i in params:
                    if str(params[i]) and str(mock_params[i]) == str(params[i]):
                        intersection_weight = intersection_weight + 1

        if intersection_weight >= 0 and intersection_weight >= max_intersection_weight:
            max_intersection_weight = intersection_weight
            result = value

    if not result:
        return None

    return format_response(result)


def normalise_path(string):
    return string.strip("/")


def format_response(cfg):
    return {
        "response": cfg["response"],
        "status": cfg["status"]
    }
