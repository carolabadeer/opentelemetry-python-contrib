import threading
import time
from random import Random
from XRaySamplerClient import XRaySamplerClient
from GetSamplingRulesResponse import SamplingRule, SamplingRuleRecord, GetSamplingRulesResponse
from GetSamplingRulesRequest import GetSamplingRulesRequest

DEFAULT_INTERVAL = 5 * 60

class RulePoller:
    def __init__(self, rule_cache, xray_client):
        self.rule_cache = rule_cache
        self.xray_client = xray_client

        self._time_elapsed = 0
        self._time_to_wait = 0
        self._cache_last_updated = 0
        # connector is XRay Sampler Client (make requests and then call getSamplingRules method)

    def start(self):
        '''start a new thread for rule polling'''
        rule_poller_thread = threading.Thread(target=self._worker)
        rule_poller_thread.daemon = True
        rule_poller_thread.start()

    def _worker(self):
        while True:
            if self._time_elapsed >= self._time_to_wait:
                self._refresh_cache()
                self._time_elapsed = 0
                self._time_to_wait = DEFAULT_INTERVAL + Random.random() * 5
            else:
                time.sleep(1)
                self._time_elapsed += 1

    def _update_rule_cache(self, rule):
        # check if rule already exists?
        # sort? check: _load_rules()
        self.rule_cache.append(SamplingRuleRecord.create(
                rule["CreatedAt"],
                rule["ModifiedAt"],
                SamplingRule.create(
                    rule["SamplingRule"]["Attributes"],
                    rule["SamplingRule"]["FixedRate"],
                    rule["SamplingRule"]["Host"],
                    rule["SamplingRule"]["HTTPMethod"],
                    rule["SamplingRule"]["Priority"],
                    rule["SamplingRule"]["ReservoirSize"],
                    rule["SamplingRule"]["ResourceARN"],
                    rule["SamplingRule"]["RuleARN"],
                    rule["SamplingRule"]["RuleName"],
                    rule["SamplingRule"]["ServiceName"],
                    rule["SamplingRule"]["ServiceType"],
                    rule["SamplingRule"]["URLPath"],
                    rule["SamplingRule"]["Version"]
                )
            ))
    
    def _refresh_cache(self):
        try:
            now = int(time.time())
            rules_response = self.xray_client.get_sampling_rules()

            # if new rules, update rule cache
            if rules_response:
                rules_response_obj = GetSamplingRulesResponse.create(rules_response["NextToken"], rules_response["SamplingRuleRecords"])
            
                for rule in rules_response_obj.get_sampling_rules():
                    self._update_rule_cache(rule)

                while rules_response["NextToken"]:
                    request = GetSamplingRulesRequest.create(rules_response["NextToken"])
                    rules_response = self.client.getSamplingRules()

                    rules_response_obj = GetSamplingRulesResponse.create(rules_response["NextToken"], rules_response["SamplingRuleRecords"])
                    for rule in rules_response_obj.get_sampling_rules():
                        self._update_rule_cache(rule)
                
                self._cache_last_updated = now

        except Exception: 
            print("Error while loading sampling rules")
    

    def _reset_time_to_wait(self):
        self._time_to_wait = DEFAULT_INTERVAL + self._random.random() * 5