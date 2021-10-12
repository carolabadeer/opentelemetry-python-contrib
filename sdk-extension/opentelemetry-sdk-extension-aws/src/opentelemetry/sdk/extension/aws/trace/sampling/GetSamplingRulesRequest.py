class GetSamplingRulesRequest:
    def __init__(self, next_token: str):
        self.next_token = next_token

    @staticmethod
    def create(next_token: str):
        return GetSamplingRulesRequest(next_token)

    def get_next_token(self) -> str:
        return self.next_token
