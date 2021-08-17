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

import sys
import random

def _fibonacci(n):
    if n in [0, 1]:
        return 1
    return _fibonacci(n - 2) + _fibonacci(n - 1)


def run(min=None, max=None):
    '''run fuka with fibonacci func'''
    if not min:
        min = 10
    if not max:
        max = random.randint(min, 30)
    fib = []
    for n in range(min, max):
        fib.append(_fibonacci(n))
    print(fib)
    return fib
