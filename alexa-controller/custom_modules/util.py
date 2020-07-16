# -*- coding: utf-8 -*-

import random
import datetime

import six
import boto3
import json


def get_random_string_from_list(input_list):
    ts = datetime.datetime.now().timestamp()
    rand = random.Random(int(ts))
    return rand.choice(input_list)
