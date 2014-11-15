#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Site-Specific Archiver Classes
from . import fourchan
from . import fuuka

default_archivers = [fourchan.FourChanSiteArchiver, fuuka.FuukaSiteArchiver]
