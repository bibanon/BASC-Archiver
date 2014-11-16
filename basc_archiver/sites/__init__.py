#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Site-Specific Archiver Classes
from __future__ import print_function
from __future__ import absolute_import

from . import fourchan
from . import fuuka

default_archivers = [fourchan.FourChanSiteArchiver, fuuka.FuukaSiteArchiver]
