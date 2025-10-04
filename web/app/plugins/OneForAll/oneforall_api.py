#!/usr/bin/env python3
# coding=utf-8

"""
Example
"""
import json

from app.plugins.OneForAll.oneforall import OneForAll


def oneforall(domain):
    test = OneForAll(target=domain)
    test.dns = True
    test.brute = True
    test.req = True
    test.takeover = False
    test.run()
    results = test.datas

    oneforall_data = []
    data = json.dumps(results)
    data = json.loads(data)
    for i in range(len(data)):
        oneforall_data.append(f"http://{data[i]['subdomain']}")
    return list(set(oneforall_data))

