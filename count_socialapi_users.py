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
  locale = payload.locale
  channel = payload.channel
  addons = payload.addons()
  hasSocial = "no"
  for addon in addons:
    if addon == "_v":
      continue;
    if addons[addon]["type"] == "service":
      hasSocial = "yes"
      break

  sessionCount = sessionActive = 0
  for day, session in payload.session_times():
    if day < "2013-06-15" or day > "2013-06-21":
      continue

    sessionCount += 1
    sessionActive += session.active_ticks

  bucket = "-".join([channel, locale, hasSocial])
  context.write("\t".join([bucket, "activeSeconds"]), sessionActive * 5)
  context.write("\t".join([bucket, "count"]), sessionCount)
  context.write("\t".join([bucket, "users"]), 1)

combine = reduce = jydoop.sumreducer
