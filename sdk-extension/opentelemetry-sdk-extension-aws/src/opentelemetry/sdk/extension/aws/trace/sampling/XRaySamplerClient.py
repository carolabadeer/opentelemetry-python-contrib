import requests
import json
class XRaySamplerClient:
    def __init__(self, host):
        self.host = host
        self.getSamplingRulesEndpoint = self.host + "/GetSamplingRules"
        self.getSamplingTargetsEndpoint = self.host + "/SamplingTargets" 

    def get_sampling_rules(self):
        r = json.dumps(
            requests.post(self.getSamplingRulesEndpoint))

        try:
            return json.loads(r) # can raise json.JSONDecodeError
        except json.JSONDecodeError:
            print("Error in retreiving JSON response")
            return r.text()


    def get_sampling_targets(self):
        r = requests.post(self.getSamplingTargetsEndpoint, data={"testKey":"testValue"})
        
        try:
            return json.loads(r)
        except json.JSONDecodeError:
            print("Error in retreiving JSON response")
            return r.text()