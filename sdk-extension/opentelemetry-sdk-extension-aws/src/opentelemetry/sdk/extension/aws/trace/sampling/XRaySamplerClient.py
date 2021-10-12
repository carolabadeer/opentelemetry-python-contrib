import requests
import json


class XRaySamplerClient:
    def __init__(self, host):
        self.host = host
        self.getSamplingRulesEndpoint = self.host + "/GetSamplingRules"
        self.getSamplingTargetsEndpoint = self.host + "/SamplingTargets"

    def get_sampling_rules(self):
        r = requests.post(self.getSamplingRulesEndpoint)

        try:
            return r.json()
        except requests.exceptions.RequestException:
            print("Error in retreiving JSON response")
            return r.text()
        except json.JSONDecodeError:
            # extra precaution to handle the event where JSON response cannot be read
            print("Error in decoding JSON response")

    def get_sampling_targets(self):
        r = requests.post(self.getSamplingTargetsEndpoint,
                          data={"testKey": "testValue"})

        try:
            return r.json()
        except requests.exceptions.RequestException:
            print("Error in retreiving JSON response")
            return r.text()
        except json.JSONDecodeError:
            print("Error in decoding JSON response")
