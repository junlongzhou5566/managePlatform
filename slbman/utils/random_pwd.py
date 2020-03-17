#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def random_str():
    seed = "23456789abcdefghjkmnpqrstuvwxyz23456789ABCDEFGHJKMNPQRSTUVWXYZ23456789"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    # print(salt)
    return salt
