# (c) 2018, Mat Wilson <mawilson@redhat.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from os import path, walk

from ansible.errors import AnsibleError
from ansible.module_utils.six import string_types
from ansible.module_utils._text import to_native, to_text
from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):

    TRANSFERS_FILES = False
    VALID_FILE_EXTENSIONS = ['csv']
    VALID_FILE_ARGUMENTS = ['file', '_raw_params']
    VALID_ALL = ['name']

    def _set_args(self):
        """ Set instance variables based on the arguments that were passed """

        self.return_results_as_name = self._task.args.get('name', None)
        self.source_file = self._task.args.get('file', None)
        if not self.source_file:
            self.source_file = self._task.args.get('_raw_params')

        self.depth = self._task.args.get('depth', None)
        self.files_matching = self._task.args.get('files_matching', None)
        self.ignore_files = self._task.args.get('ignore_files', None)
        self.valid_extensions = self._task.args.get('extensions', self.VALID_FILE_EXTENSIONS)

        # convert/validate extensions list
        if isinstance(self.valid_extensions, string_types):
            self.valid_extensions = list(self.valid_extensions)
        if not isinstance(self.valid_extensions, list):
            raise AnsibleError('Invalid type for "extensions" option, it must be a list')

    def run(self, tmp=None, task_vars=None):
        """ Load yml files recursively from a directory.
        """
        del tmp  # tmp no longer has any effect

        if task_vars is None:
            task_vars = dict()

        self.show_content = True
        self.included_files = []

        # Validate arguments
        files = 0
        for arg in self._task.args:
            if arg in self.VALID_FILE_ARGUMENTS:
                files += 1
            elif arg in self.VALID_ALL:
                pass
            else:
                raise AnsibleError('{0} is not a valid option in debug'.format(arg))

        # set internal vars from args
        self._set_args()

        results = dict()

        try:
            self.source_file = self._find_needle('vars', self.source_file)
            failed, err_msg, updated_results = (
                self._load_files(self.source_file)
            )
            if not failed:
                results.update(updated_results)

        except AnsibleError as e:
            failed = True
            err_msg = to_native(e)

        if self.return_results_as_name:
            scope = dict()
            scope[self.return_results_as_name] = results
            results = scope

        result = super(ActionModule, self).run(task_vars=task_vars)

        if failed:
            result['failed'] = failed
            result['message'] = err_msg

        result['ansible_included_var_files'] = self.included_files
        result['ansible_facts'] = results
        result['_ansible_no_log'] = not self.show_content

        return result

