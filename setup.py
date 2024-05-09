# Python package for LZSS encoding/decoding - setup.py
#
# Copyright (C) 2013 Plastic Logic Limited
#
#     Guillaume Tucker <guillaume.tucker@plasticlogic.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path

from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            'lzss',
            sources=[str(Path('src/pylzss.c'))],
            include_dirs=[str(Path('src/include'))]
        )
    ]
)
