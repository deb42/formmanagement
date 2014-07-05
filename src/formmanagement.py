# encoding: utf-8
from __future__ import absolute_import, print_function, division, unicode_literals

import argparse
import os
from libformmanagement import app
from libformmanagement.seed import seed

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=os.path.abspath('./config_dev.py'), help='Configuration file to use')
    options = parser.parse_args()

    # Initialize Flask object
    app.config.from_pyfile(options.config)

    seed()

    app.run(threaded=True)