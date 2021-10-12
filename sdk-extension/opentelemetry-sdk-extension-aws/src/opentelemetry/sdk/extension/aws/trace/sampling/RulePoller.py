import threading
import time
from random import random
from XRaySamplerClient import XRaySamplerClient
from GetSamplingRulesResponse import SamplingRule, SamplingRuleRecord, GetSamplingRulesResponse
from GetSamplingRulesRequest import GetSamplingRulesRequest

DEFAULT_INTERVAL = 5 * 60


class RulePoller:
    def __init__(self, rule_cache: list, xray_client: XRaySamplerClient):
        self.rule_cache = rule_cache
        self.xray_client = xray_client  # connector (from AWS XRay Rule Poller)

        self._time_elapsed = 0
        self._time_to_wait = 0
        self._cache_last_updated = 0

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
                self._time_to_wait = DEFAULT_INTERVAL + random() * 5
            else:
                time.sleep(1)
                self._time_elapsed += 1

    def _update_rule_cache(self, rule):
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
            # print(rules_response)

            # if new rules, update rule cache
            if rules_response:
                rules_response_obj = GetSamplingRulesResponse.create(
                    rules_response["NextToken"], rules_response["SamplingRuleRecords"])

                for rule in rules_response_obj.get_sampling_rules():
                    self._update_rule_cache(rule)

                # next response would not exist in last response
                while "NextToken" in rules_response:
                    request = GetSamplingRulesRequest.create(
                        rules_response["NextToken"])

                    rules_response = self.xray_client.get_sampling_rules()
                    # print(rules_response)

                    rules_response_obj = GetSamplingRulesResponse.create(
                        rules_response["NextToken"], rules_response["SamplingRuleRecords"])
                    for rule in rules_response_obj.get_sampling_rules():
                        self._update_rule_cache(rule)

                self._cache_last_updated = now

        except Exception:
            print("Error while loading sampling rules")

    def _reset_time_to_wait(self):
        self._time_to_wait = DEFAULT_INTERVAL + random() * 5
