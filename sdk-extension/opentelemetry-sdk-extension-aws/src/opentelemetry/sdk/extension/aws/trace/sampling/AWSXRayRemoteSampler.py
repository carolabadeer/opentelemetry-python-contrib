from logging import getLogger
from types import MappingProxyType
from typing import Optional, Sequence
from opentelemetry import trace

# pylint: disable=unused-import
from opentelemetry.context import Context
from opentelemetry.trace import Link, SpanKind, get_current_span
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes


# import classes from sampling.py instead later
from opentelemetry.sdk.trace.sampling import Decision, Sampler, SamplingResult, TraceIdRatioBased
from opentelemetry.sdk.extension.aws.trace.sampling import XRaySamplerClient

# same as java class name
class AWSXRayRemoteSampler(Sampler):
    def __init__(self, endpoint, sampler=TraceIdRatioBased(0.05)):
        self.receiver_endpoint = endpoint 
        self.sampler = sampler

        self.client = XRaySamplerClient(endpoint)

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
    
    def _getAndUpdateSampler(self):
        # keep track of previous response & check if they are the same 
        rules_response = self.client.getSamplingRules()
    
    def _generateClientID():
        pass
