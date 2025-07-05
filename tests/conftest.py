#!/usr/bin/env python

import os

import git
import pytest


@pytest.fixture
def get_repo():
    """
    Get repo class object 'git.repo.base.Repo'

    Return: repo object
    """
    repo_path = os.getcwd()
    repo = git.Repo(repo_path)

    return repo
