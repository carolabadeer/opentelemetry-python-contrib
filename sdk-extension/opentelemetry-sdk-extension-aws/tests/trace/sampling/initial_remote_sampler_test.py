# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.extension.aws.trace import AwsXRayIdGenerator
import logging

# import new remote sampler 
from opentelemetry.sdk.extension.aws.trace.sampling import AWSXRayRemoteSampler


logging.basicConfig(level='DEBUG')

# instantiate new remote sampler 
remote_sampler = AWSXRayRemoteSampler(endpoint="http://localhost:2000")

# OpenTelemetry collector
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)


processor = SimpleSpanProcessor(otlp_exporter)
provider = TracerProvider(active_span_processor=processor, id_generator=AwsXRayIdGenerator(), sampler=remote_sampler)
# provider.add_span_processor(processor)
trace.set_tracer_provider(provider)


tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("foo"):
    with tracer.start_as_current_span("bar"):
        with tracer.start_as_current_span("baz"):
            print("Hello world from OpenTelemetry Python!")

# opentelemetry-python-contrib/sdk-extension/opentelemetry-sdk-extension-aws/tests/trace/sampling