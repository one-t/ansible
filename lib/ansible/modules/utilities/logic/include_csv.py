#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Mat Wilson <mathew.david.wilson@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: include_csv

short_description: Load a list of dictionaries from a csv file, dynamically within a task.

version_added: "2.6"

description:
  - Take a CSV (Comma Separated Values) file and store all of the rows
    as a list of dictionaries

options:
  file:
    description:
      - The file name from which comma separated rows will be loaded
      - If the path is relative, it will look for the file in vars/ subdirectory of a role or relative to playbook.
    required: true
  name:
    version_added: "2.2"
    description:
      - The name of a variable into which assign the included vars. If omitted (null) they will be made top level vars.

author:
    - Mat Wilson (@one-t)
'''

EXAMPLES = """
- name: Include rows of stuff.csv into the 'stuff' variable.
  include_csv:
    file: stuff.csv
    name: stuff
"""

RETURN = '''
ansible_facts:
    description: Variables that were included and their values
    type: list
    returned: success
    sample:
      - {'variable': 'value'}
      - {'variable': 'value'}
ansible_included_csv_files:
    description: A list of files that were successfully included
    returned: success
    type: list
    sample: [ '/path/to/file.csv', '/path/to/file.csv' ]
'''
