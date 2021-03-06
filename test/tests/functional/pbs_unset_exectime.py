# coding: utf-8

# Copyright (C) 1994-2020 Altair Engineering, Inc.
# For more information, contact Altair at www.altair.com.
#
# This file is part of both the OpenPBS software ("OpenPBS")
# and the PBS Professional ("PBS Pro") software.
#
# Open Source License Information:
#
# OpenPBS is free software. You can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# OpenPBS is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Commercial License Information:
#
# PBS Pro is commercially licensed software that shares a common core with
# the OpenPBS software.  For a copy of the commercial license terms and
# conditions, go to: (http://www.pbspro.com/agreement.html) or contact the
# Altair Legal Department.
#
# Altair's dual-license business model allows companies, individuals, and
# organizations to create proprietary derivative works of OpenPBS and
# distribute them - whether embedded or bundled with other software -
# under a commercial license agreement.
#
# Use of Altair's trademarks, including but not limited to "PBS™",
# "OpenPBS®", "PBS Professional®", and "PBS Pro™" and Altair's logos is
# subject to Altair's trademark licensing policies.


from tests.functional import *


class Testunset_exectime(TestFunctional):
    """
    Test that unsetting execution time through hooks does not throw parse error
    """

    def test_unset_exectime(self):
        """
        Create a hook to unset execution time and check after submitting
        a job no error messages are logged
        """
        hook_name = "exechook"
        hook_body = """
import pbs
e = pbs.event()
if (e.type is pbs.QUEUEJOB):
        o = e.job
        o.Execution_Time = None
else:
        e.reject("unmatched event type!")
"""
        a = {'event': 'queuejob', 'enabled': 'True'}
        self.server.create_import_hook(hook_name, a, hook_body)
        self.server.manager(MGR_CMD_SET, SERVER, {'log_events': 2047})
        j = Job(TEST_USER)
        self.server.submit(j)
        msg = "Error evaluating Python script, "
        msg += "exec_time could not be parsed"
        self.server.log_match(msg, max_attempts=5, existence=False)
