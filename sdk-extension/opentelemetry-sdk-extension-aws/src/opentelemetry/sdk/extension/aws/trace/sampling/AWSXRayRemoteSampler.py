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
from RulePoller import RulePoller

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
    
    def _get_and_update_sampling_rules(self):
        # start rule polling 
        rule_poller = RulePoller(self.rule_cache, self.client)
        rule_poller.start()