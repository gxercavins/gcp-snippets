# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from random import randint
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


class LottoPage(webapp2.RequestHandler):
    def get(self):
        lucky_combination = []
        repeat = True

        for i in range(6):
            while (repeat):
                num = randint(1,49)
                if num in lucky_combination:
                    repeat = True
                else:
                    repeat = False  
            lucky_combination.append(num)
            repeat = True

        logging.info(sorted(lucky_combination))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(sorted(lucky_combination))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/lotto', LottoPage),
], debug=True)

