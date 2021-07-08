import requests

class XRaySamplerClient:
    def __init__(self, host):
        self.host = host
        self.getSamplingRulesEndpoint = self.host + "/GetSamplingRules"
        self.getSamplingTargetsEndpoint = self.host + "/SamplingTargets" 

    def getSamplingRules(self):
        # empty JSON data object
        r = requests.post(self.getSamplingRulesEndpoint)

        # can raise json.JSONDecodeError 
        #print(r.json())

    def getSamplingTargets(self):
        r = requests.post(self.getSamplingTargetsEndpoint, data={"testKey":"testValue"})
        #print(r.json())