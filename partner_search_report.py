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
import orphUtils

from healthreportutils import (
    FHRMapper,
    setupjob,
)

@orphUtils.localTextInput()
@FHRMapper()
def map(key, rawJsonIn, context):
    channel = rawJsonIn.channel
    
    version = str(rawJsonIn.app_version)

    for day, engine, where, count in rawJsonIn.daily_search_counts():
      context.write('\t'.join((channel, version, engine, where)), count)

combine = reduce = jydoop.sumreducer
