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
    os = payload.os
    os_ver = payload.os_version
    cpu = payload.cpu_arch
    cpu_cores = str(payload.cpu_cores)
    mem = payload.memory
    if mem == "NaN":
        return

    if mem >= 32768:
        mem = 32768
    elif mem >= 16384:
        mem = 16384
    elif mem >= 8192:
        mem = 8192
    elif mem >= 4096:
        mem = 4096
    elif mem >= 2048:
        mem = 2048
    elif mem >= 1024:
        mem = 1024
    elif mem >= 512:
        mem = 512
    else:
        mem = 256

    memStr = str(mem)

    context.write('\t'.join((channel, cpu, cpu_cores, memStr, os, os_ver)), 1)

combine = reduce = jydoop.sumreducer
