class GetSamplingRulesResponse:
    def __init__(self, next_token: str, sampling_rules: list):
        self.next_token = next_token
        self.sampling_rules = sampling_rules
    
    @staticmethod
    def create(next_token: str, sampling_rules: list):
        return GetSamplingRulesResponse(next_token, sampling_rules)

    def get_next_token(self) -> str:
        return self.next_token 

    def get_sampling_rules(self) -> list:
        '''returns a list of SamplingRuleRecords, which are defined in the class below''' 
        return self.sampling_rules 


class SamplingRuleRecord:
    def __init__(self, created_at: str, modified_at: str, sampling_rule):
        self.created_at = created_at
        self.modified_at = modified_at
        self.sampling_rule = sampling_rule
    
    @staticmethod
    def create(created_at: str, modified_at: str, sampling_rule):
        return SamplingRuleRecord(created_at, modified_at, sampling_rule)

    def get_created_at(self) -> str:
        return self.created_at 

    def get_modified_at(self) -> str:
        return self.modified_at

    def get_sampling_rule(self):
        return self.sampling_rule 


class SamplingRule:
    def __init__(self, attributes: dict, fixed_rate: float, host: str, http_method: str, 
            priority: int, reservoir_size: int, resource_arn: str, rule_arn: str, rule_name: str,
            service_name: str, service_type: str, url_path: str, version: int):
        self.attributes = attributes
        self.fixed_rate = fixed_rate
        self.host = host
        self.http_method = http_method 
        self.priority = priority
        self.reservoir_size = reservoir_size
        self.resource_arn = resource_arn
        self.rule_arn = rule_arn
        self.rule_name = rule_name 
        self.service_name = service_name
        self.service_type = service_type
        self.url_path = url_path
        self.version = version

    @staticmethod 
    def create(attributes: dict, fixed_rate: float, host: str, httpMethod: str, 
            priority: int, reservoir_size: int, resource_arn: str, rule_arn: str, rule_name: str,
            service_name: str, service_type: str, url_path: str, version: int):

        return SamplingRule(attributes, fixed_rate, host, httpMethod, priority, reservoir_size, resource_arn, rule_arn, rule_name, service_name, 
        service_type, url_path, version)

    def get_attributes(self) -> dict:
        return self.attributes

    def get_fixed_rate(self) -> float:
        return self.fixed_rate

    def get_host(self) -> str:
        return self.host 

    def get_http_method(self) -> str:
        return self.http_method

    def get_priority(self) -> int:
        return self.priority
    
    def get_reservoir_size(self) -> int:
        return self.reservoir_size
    
    def get_resource_arn(self) -> str:
        return self.resource_arn

    def get_rule_arn(self) -> str:
        return self.rule_arn

    def get_rule_name(self) -> str:
        return self.rule_name
    
    def get_service_name(self) -> str:
        return self.service_name

    def get_service_type(self) -> str:
        return self.service_type

    def get_url_path(self) -> str:
        return self.url_path

    def get_version(self) -> int:
        return self.version