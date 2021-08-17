from logging import getLogger
from types import MappingProxyType
from typing import Optional, Sequence
from opentelemetry import trace

# pylint: disable=unused-import
from opentelemetry.context import Context
from opentelemetry.trace import Link, SpanKind, get_current_span
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace.sampling import Decision, Sampler, SamplingResult, TraceIdRatioBased

from XRaySamplerClient import XRaySamplerClient
from GetSamplingRulesResponse import SamplingRule, SamplingRuleRecord, GetSamplingRulesResponse
from GetSamplingRulesRequest import GetSamplingRulesRequest

class AWSXRayRemoteSampler(Sampler):
    def __init__(self, resource, endpoint="http://localhost:2000", sampler=TraceIdRatioBased(0.05)):
        self.receiver_endpoint = endpoint 
        self.initial_sampler = sampler
        self.resource = resource

        self.client = XRaySamplerClient(endpoint)

        self.rule_cache = []
    
    def should_sample(
        self,
        parent_context: Optional["Context"],
        trace_id: int,
        name: str,
        kind: SpanKind = None,
        attributes: Attributes = None,
        links: Sequence["Link"] = None,
        trace_state: "TraceState" = None,
    ) -> "SamplingResult":

        return self.sampler.should_sample(parent_context, trace_id, name, kind, attributes, links, trace_state)
     
    def get_description(self) -> str:
        return "AwsXrayRemoteSampler{" + self.sampler.getDescription() + "}"

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
    
    def _get_and_update_sampling_rules(self):
        rules_response = self.client.getSamplingRules()
        rules_response_obj = GetSamplingRulesResponse.create(rules_response["NextToken"], rules_response["SamplingRuleRecords"])
        print("next token parsed", rules_response_obj.get_next_token())

        for rule in rules_response_obj.get_sampling_rules():
            self._update_rule_cache(rule)


        while rules_response["NextToken"]:
            request = GetSamplingRulesRequest.create(rules_response["NextToken"])
            rules_response = self.client.getSamplingRules()

            rules_response_obj = GetSamplingRulesResponse.create(rules_response["NextToken"], rules_response["SamplingRuleRecords"])
            for rule in rules_response_obj.get_sampling_rules():
                self._update_rule_cache(rule)


    def _generate_client_ID():
        pass
