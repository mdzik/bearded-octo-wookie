# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 18:03:28 2015

@author: michal
"""

import os, subprocess
import datetime

"""
https://github.com/warner/python-ecdsa/blob/9e21c3388cc98ba90877a1e4dbc2aaf66c67d365/setup.py#L33
"""

VERSION_PY = """
# This file is originally generated from Git information by running 'setup.py
# version'.
__version__ = '%s'
__date__ = '%s'
"""
def update_version_py():
    if not os.path.isdir(".git"):
        print "This does not appear to be a Git repository."
        import bearded_octo_wookie._bow_version
        return bearded_octo_wookie._bow_version.__version__
    try:
        p = subprocess.Popen(["git", "describe",
                              "--tags", "--dirty", "--always"],
                             stdout=subprocess.PIPE)
    except EnvironmentError:
        print "unable to run git, leaving ecdsa/_version.py alone"
        return
    stdout = p.communicate()[0]
    
    if p.returncode != 0:
        print "unable to run git, leaving ecdsa/_version.py alone"
        return
    # we use tags like "python-ecdsa-0.5", so strip the prefix
#    assert stdout.startswith("python-ecdsa-")
    #ver = stdout[len("python-ecdsa-"):].strip()
    ver = stdout[:-1]
    f = open("_bow_version.py", "w")
    f.write(VERSION_PY % (ver, datetime.time() ) )
    f.close()
    print "set _version.py to '%s'" % ver
    



