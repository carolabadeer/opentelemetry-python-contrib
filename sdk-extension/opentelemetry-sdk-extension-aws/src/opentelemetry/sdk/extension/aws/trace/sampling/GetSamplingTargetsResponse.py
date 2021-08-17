class GetSamplingTargetsResponse:
    def __init__(self, last_rule_modification, sampling_target_documents, unprocessed_statistics):
        self.last_rule_modification = last_rule_modification
        self.sampling_target_documents = sampling_target_documents
        self.unprocessed_statistics = unprocessed_statistics

    @staticmethod
    def create(last_rule_modification, sampling_target_documents, unprocessed_statistics):
        return GetSamplingTargetsResponse(last_rule_modification, sampling_target_documents, unprocessed_statistics)
    
    def get_last_rule_modification(self):
        return self.last_rule_modification
    
    def get_sampling_target_documents(self):
        return self.sampling_target_documents
    
    def get_unprocessed_statistics(self):
        return self.unprocessed_statistics

class SamplingTargetDocument:
    def __init__(self, fixed_rate: float, interval: int, reservoir_quota: int, reservoir_quota_TTL, rule_name: str):
        self.fixed_rate = fixed_rate
        self.interval = interval
        self.reservoir_quota = reservoir_quota
        self.reservoir_quota_TTL = reservoir_quota_TTL
        self.rule_name = rule_name

    @staticmethod
    def create(fixed_rate: float, interval: int, reservoir_quota: int, reservoir_quota_TTL, rule_name: str):
        return SamplingTargetDocument(fixed_rate, interval, reservoir_quota, reservoir_quota_TTL, rule_name)
    
    def get_fixed_rate(self) -> float:
        return self.fixed_rate
    
    def get_interval(self) -> int:
        return self.interval

    def get_reservoir_quota(self) -> int:
        return self.reservoir_quota
    
    def get_reservoir_quota_TTL(self):
        # convert to date?
        return self.reservoir_quota_TTL
    
    def get_rule_name(self) -> str:
        return self.rule_name

class UnprocessedStatistics:
    def __init__(self, error_code: str, message: str, rule_name: str):
        self.error_code = error_code
        self.message = message 
        self.rule_name = rule_name

    @staticmethod
    def create(error_code: str, message: str, rule_name: str):
        return UnprocessedStatistics(error_code, message, rule_name)

    def get_error_code(self):
        return self.error_code
    
    def get_message(self):
        return self.message 

    def get_rule_name(self):
        return self.rule_name