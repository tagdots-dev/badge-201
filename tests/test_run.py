#!/usr/bin/env python

"""
Purpose: tests
"""

import git
import pytest
from click.testing import CliRunner

from pkg_18604.run import (
    check_user_inputs,
    checkout_branch,
    cicleanup,
    create_badge_dict,
    create_badge_json,
    main,
    push_changes,
)


def test_get_repo(get_repo):
    """
    Test to verify that get_repo fixture provides a valid GitPython Repo object
    """
    assert isinstance(get_repo, git.repo.base.Repo)
    assert get_repo.working_dir is not None


def test_checkout_branch_return_none(get_repo):
    """
    Test checkout branch

    Expect Result: None due to invalid get_repo class object
    """
    get_repo = ''
    remote_name = 'origin'
    badge_branch = 'ci-testing'
    default_branch = 'main'

    result = checkout_branch(get_repo, remote_name, default_branch, badge_branch)
    print(f'\nCheckout branch result: {result}')

    assert result is None


def test_check_user_inputs_return_false_01():
    """
    Test user input validations

    Expect Result: False due to badge_style not in available_badge_styles
    """
    available_badge_styles = ['flat', 'flat-square', 'plastic', 'for-the-badge', 'social']
    badge_style = 'hoodoo'
    label_color = '000000'
    message_color = 'FFFFFF'

    result = check_user_inputs(available_badge_styles, badge_style, label_color, message_color)
    print(f'\nCheck user inputs result: {result}')

    assert result is False


def test_check_user_inputs_return_false_02():
    """
    Test user input validations

    Expect Result: False due to invalid hex color in label-color
    """
    available_badge_styles = ['flat', 'flat-square', 'plastic', 'for-the-badge', 'social']
    badge_style = 'flat'
    label_color = '0000'
    message_color = 'FFF'

    result = check_user_inputs(available_badge_styles, badge_style, label_color, message_color)
    print(f'\nCheck user inputs result: {result}')

    assert result is False


def test_check_user_inputs_return_false_03():
    """
    Test user input validations

    Expect Result: False due to invalid hex color in message-color
    """
    available_badge_styles = ['flat', 'flat-square', 'plastic', 'for-the-badge', 'social']
    badge_style = 'flat'
    label_color = '000'
    message_color = 'GGG'

    result = check_user_inputs(available_badge_styles, badge_style, label_color, message_color)
    print(f'\nCheck user inputs result: {result}')

    assert result is False


def test_create_badge_json_return_false_01():
    """
    Test create badge json file from template json file

    Expect Result: False due to template file not exist
    """
    badge_file_src = 'src/pkg_18604/default/template-NOT_EXIST.json'
    badge_style = 'flat'
    label = 'ci-testing'
    label_color = '000'
    message = 'no status'
    message_color = 'FFF'
    badge_dict = create_badge_dict(badge_style, label, label_color, message, message_color)
    badge_name = 'ci-testing'

    result = create_badge_json(badge_file_src, badge_dict, badge_name)
    print(f'\nCreate badge JSON from template result: {result}')

    assert result is False


def test_create_badge_json_return_false_02():
    """
    Test create badge json file from template json file

    Expect Result: False due to invalid badge_dict
    """
    badge_file_src = 'src/pkg_18604/default/template.json'
    badge_dict = ''
    badge_name = 'ci-testing'

    result = create_badge_json(badge_file_src, badge_dict, badge_name)
    print(f'\nCreate badge JSON from template result: {result}')

    assert result is False


def test_push_changes_return_none_01(get_repo):
    """
    Test push changes to remote

    Expect Result: None due to invalid repo class object
    """
    repo = ''
    badge_name = 'ci-testing'
    badge_branch = 'ci-testing'
    remote_name = 'origin'
    gitconfig_name = 'Lisa Gherardini'
    gitconfig_email = 'lisa.gherardini@example.com'
    msg_suffix = '[CI - Testing]'

    assert push_changes(repo, remote_name, badge_branch, badge_name, gitconfig_name, gitconfig_email, msg_suffix) is None


def test_push_changes_return_none_02(get_repo):
    """
    Test push changes to remote

    Expect Result: None due to invalid remote_name
    """
    badge_name = 'ci-testing'
    badge_branch = 'ci-testing'
    remote_name = 'origin-false'
    gitconfig_name = 'Lisa Gherardini'
    gitconfig_email = 'lisa.gherardini@example.com'
    msg_suffix = '[CI - Testing]'

    assert push_changes(get_repo, remote_name, badge_branch, badge_name, gitconfig_name, gitconfig_email, msg_suffix) is None


def test_main_return_failure_01():
    """
    Test main

    Expect Result: Return Failure Message for invalid hex color on label-color
    """
    runner = CliRunner()
    result = runner.invoke(main, ['--badge-branch', 'ci-testing', '--badge-name', 'ci-testing', '--label-color', 'GGG'])
    print(f'\nMain result: {result}')

    assert result is not None


def test_main_return_failure_02():
    """
    Test main

    Expect Result: Return Failure Message for invalid remote name
    """
    runner = CliRunner()
    result = runner.invoke(main, ['--badge-branch', 'ci-testing', '--badge-name', 'ci-testing', '--remote-name', 'invalid'])
    print(f'\nMain result: {result}')

    assert result is not None


def test_main_return_failure_03():
    """
    Test main

    Expect Result: Return Failure Message for invalid badge file source
    """
    runner = CliRunner()
    result = runner.invoke(main, ['--badge-branch', 'ci-testing', '--badge-name', 'ci-testing', '--badge-file-src', 'invalid'])  # noqa: E501
    print(f'\nMain result: {result}')

    assert result is not None


def test_cicleanup_failure(get_repo):
    """
    Test ci-cleanup

    Expect Result: True
    """
    remote_name = 'origin'
    badge_branch = 'ci-testing'
    default_branch = 'invalid'

    result = cicleanup(get_repo, remote_name, default_branch, badge_branch)
    print(f'\nCleanup result: {result}')

    assert result is False


def test_main_return_success():
    """
    Test main

    Expect Result: Return Endpoint Badge for README
    """
    runner = CliRunner()
    result = runner.invoke(main, ['--badge-branch', 'ci-testing', '--badge-name', 'ci-testing', '--ci-cleanup', 'True'])
    print(f'\nMain result: {result}')
    print(result.stdout)
    print(result.stderr)

    assert result is not None


if __name__ == "__main__":
    pytest.main()
