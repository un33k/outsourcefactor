#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings.test'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)

