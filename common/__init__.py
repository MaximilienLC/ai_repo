"""Contains functionality common to multiple projects."""

from beartype import BeartypeConf
from beartype.claw import beartype_this_package

beartype_this_package(conf=BeartypeConf(is_pep484_tower=True))
