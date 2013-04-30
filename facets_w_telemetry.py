# Copyright 2013 The Mozilla Foundation <http://www.mozilla.org/>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import jydoop

from healthreportutils import (
    FHRMapper,
    setupjob,
)


@FHRMapper()

def map(key, payload, context):
    channel = payload.channel
    locale = payload.locale
    os = payload.os + payload.os_version
    if payload.telemetry_enabled:
      telemetryEnabled =  "enabled"
    else: 
      telemetryEnabled = "disabled"

    context.write('\t'.join((telemetryEnabled, os, channel)), 1)

combine = reduce = jydoop.sumreducer
