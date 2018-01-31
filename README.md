# LINKS

[PyPi page](https://pypi.python.org/pypi/api-cloudvps-py)

[github](https://github.com/wa-pis/api-cloudvps-py)

[wiki]

# INSTALLING

```
#!bash

$ pip install api-cloudvps-py
# or use source code package, after extract
$ python setup.py install
```

# How to obtain token

If you want to work with reg.ru cloudvps api client [participate](https://www.reg.ru/company/news/9009)

# USAGE

```
#!python

# import
>>> from cloudvps import Api
>>> api = Api('3f7c0a3d*****356b45d59f71a')
# or
>>> import cloudvps
>>> api = cloudvps.Api('3f7c0a3d*****356b45d59f71a')
>>> common = api.common
>>> print(common.sizes())
{'sizes': [{'disk': 20, 'id': 5, 'memory': 512, 'name': 'Меркурий', 'slug': 'test_512', 'vcpus': 1, 'weight': 10}, {'disk': 30, 'id': 1, 'memory': 1024, 'name': 'Марс', 'slug': 'test', 'vcpus': 1, 'weight': 20}, {'disk': 40, 'id': 3, 'memory': 2048, 'name': 'Венера', 'slug': 'test_x2', 'vcpus': 2, 'weight': 30}]}

```

# LICENSE
The MIT License (MIT)

Copyright © 2017, Anton Grudin.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
