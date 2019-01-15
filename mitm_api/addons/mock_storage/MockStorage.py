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

    def get_mock(self):  # , service: str, method: str, command: str, params):
        pre_results = []

        for value in self.configs:
            if not ("service" in value and value["service"]):
                continue

            print(value)


"""
export function getMatchedConfig(this:void, service:string, method:string, command:string, params:{ [i:string]:number | string | boolean }, configs:IConfig[]):{ response:any, status:number } {
    const pre_results = [];

    for (const value of configs) {
        if (!(value.service && value.service === service)) {
            continue;
        }

        if (value.method !== method) {
            continue;
        }

        const norm_command = normalisePath(command);
        const norm_value_command = normalisePath(value.command);

        if (norm_command === norm_value_command) {
            pre_results.push(value);
        }
    }

    if (Object.keys(params || {}).length === 0) {
        const empty_results = pre_results.filter((cfg:IConfig) => {
            return Object.keys(cfg.params).length === 0;
        });

        if (empty_results.length > 0) {
            return formatResponse(empty_results[0]);
        }

        return undefined;
    }

    let max_intersection_weight = 0;
    let result;

    for (const value of pre_results) {
        let intersection_weight = 0;

        for (const i in value.params) {
            if(value.params[i] && params[i]) {
                if (params[i].toString && value.params[i].toString() === params[i].toString()) {
                    intersection_weight++;
                }
            }
        }

        if (intersection_weight >= 0 && intersection_weight >= max_intersection_weight) {
            max_intersection_weight = intersection_weight;
            result = value;
        }
    }

    if (!result) {
        return undefined;
    }

    return formatResponse(result);
}
"""
