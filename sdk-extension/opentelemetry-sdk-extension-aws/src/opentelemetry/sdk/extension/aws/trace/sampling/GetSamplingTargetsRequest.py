class GetSamplingTargetsRequest:
    def __init__(self, statistic_documents):
        self.statistic_documents = statistic_documents

    @staticmethod
    def create(statistic_documents):
        return GetSamplingTargetsRequest(statistic_documents)

    def get_statistic_documents(self):
        return self.statistic_documents


class SamplingStatisticsDocument:
    def __init__(self, borrow_count: int, client_ID:  str, request_count: int, rule_name: str, sampled_count: int, timestamp: int):
        # timestamp type int or date?
        self.borrow_count = borrow_count
        self.client_ID = client_ID
        self.request_count = request_count
        self.rule_name = rule_name
        self.sampled_count = sampled_count
        self.timestamp = timestamp
    
    @staticmethod
    def create(borrow_count: int, client_ID:  str, request_count: int, rule_name: str, sampled_count: int, timestamp: int):
        return SamplingStatisticsDocument(borrow_count, client_ID, request_count, rule_name, sampled_count, timestamp)
    
    def get_borrow_count(self):
        return self.borrow_count
    
    def get_client_ID(self):
        return self.client_ID
    
    def get_request_count(self):
        return self.request_count
    
    def get_rule_name(self):
        return self.rule_name 

    def get_sampled_count(self):
        return self.sampled_count
    
    def get_timestamp(self):
        # separate function to convert timestamp to a date??
        return self.timestamp
