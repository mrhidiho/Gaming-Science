"""Reference adapters matching the eight student exercise contracts."""
from .cache import cache_hits
from .models import pareto_front, setup_slack, hold_slack
from .ecc import encode as ecc_encode, decode as ecc_decode
from .analysis import paired_gmean
from .security import descriptor_valid
