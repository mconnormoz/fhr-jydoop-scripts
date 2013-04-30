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
    addons = payload.current_addons
    services = []

    if type(addons) != dict:
      return
    if channel != "nightly":
      return

    for addon in addons:
      if type(addons[addon]) != dict:
        continue

      if addons[addon]['type'] == 'service':
        services.append(addon)

    ticks = 0;
    sessions = 0;
    for day, session in payload.session_times():
      date = day.split("-")
      if int(date[1]) < 4:
        continue
      elif int(date[2]) < 16:
        continue
      sessions += 1
      ticks += session[2]

    if sessions > 0:
      svcs = ",".join(services)
      if svcs == "":
        svcs = "none"
      context.write("\t".join((svcs, "users")), 1)
      context.write("\t".join((svcs, "sessions")), sessions)
      context.write("\t".join((svcs, "seconds")), ticks * 12)

combine = reduce = jydoop.sumreducer
