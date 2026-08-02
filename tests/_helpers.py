"""Shared setup and assertions for the generator self-checks.

Importing this puts the repo root on the working directory and `scripts/` on the
path, so a test is just `mod, entries = load('talks')` plus its own spot-checks.
"""
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))


def load(name):
    """Import a generator module and parse its DATA file: -> (module, entries)."""
    module = __import__(name)
    return module, read(module.DATA)


def read(path):
    """Parse a YAML data file (for modules with more than one DATA path)."""
    with open(path, encoding='utf-8') as fh:
        return yaml.safe_load(fh)


def assert_itemize(tex, n_items):
    """The checks every CV .tex fragment shares."""
    assert tex.startswith('% GENERATED'), 'missing provenance header'
    assert tex.count('\\item') == n_items, f'expected {n_items} \\item entries'
    assert tex.rstrip().endswith('\\end{itemize}')
