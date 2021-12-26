from jsondiff import diff

import sys
import json
from colorama import init
from colorama import Fore


def validate(testName, ignored, template):
    init()
    print(Fore.BLUE, testName, Fore.RED, sep="")

    response = json.loads(sys.stdin.read())

    for name in ignored:
        if name in response:
            del response[name]

    d = diff(template, response)
    if len(d) != 0:
        print(Fore.RED, d)
        return 1
    else:
        print(Fore.GREEN, "Good")
        return 0
