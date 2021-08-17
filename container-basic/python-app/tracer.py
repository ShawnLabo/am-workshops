import opencensus
import opencensus.trace.tracer as tracer
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
import os

def init():
    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')

    exporter = stackdriver_exporter.StackdriverExporter(
        project_id=project_id,
        # transport=BackgroundThreadTransport
    )
    tracer = opencensus.trace.tracer.Tracer(
        exporter=exporter,
        sampler=opencensus.trace.samplers.AlwaysOnSampler()
    )

    return tracer