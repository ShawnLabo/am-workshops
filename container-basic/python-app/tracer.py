# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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