#!/usr/bin/env python
import nose
import logging
l = logging.getLogger("angr_tests")

try:
    # pylint: disable=W0611,F0401
    import standard_logging
    import angr_debug
except ImportError:
    pass

import angr

# load the tests
import os
test_location = str(os.path.dirname(os.path.realpath(__file__)))
strncpy_amd64 = None

def setup_module():
    setup_amd64()

def setup_amd64():
    global strncpy_amd64
    strncpy_amd64 = angr.Project(test_location + "/blob/x86_64/strncpy", load_options={'auto_load_libs': True}, exclude_sim_procedures=['strncpy'])

def test_amd64():
    explorer = angr.surveyors.Explorer(strncpy_amd64, find=[0x4005FF]).run()
    s = explorer.found[0].state
    result = s.se.any_str(s.mem_expr(s.reg_expr(16), 16))
    nose.tools.assert_equals(result, 'why hello there\x00')

if __name__ == "__main__":
    setup_amd64()
    test_amd64()
