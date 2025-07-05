#!/usr/bin/env python

"""
Purpose: Generate a shields.io endpoint badge
"""

import os

import click
import git

from pkg_18604 import __version__


def get_repo():  # pragma: no cover
    """
    Get repo class object 'git.repo.base.Repo'

    Return: repo object
    """
    repo_path = os.getcwd()
    repo = git.Repo(repo_path)
    return repo


def checkout_branch(repo, remote_name, default_branch, badge_branch):
    """
    Remote branch exists?
    If yes, checkout remote branch to local
    If no , checkout a new local branch

    Parameter(s):
    repo          : repo class object 'git.repo.base.Repo'
    remote_name   : remote name (e.g. origin)
    badge_branch  : badge branch name (e.g. badges)
    default_branch: default branch of the repo (e.g. main)

    Return: branch object '<class 'git.refs.head.Head'>' or None
    """
    try:
        origin = repo.remote(name=remote_name)
        origin.fetch(prune=True)

        if any(ref.name == f'{remote_name}/{badge_branch}' for ref in origin.refs):
            remote_branch = f'{remote_name}/{badge_branch}'
            local_branch = repo.create_head(badge_branch, remote_branch)
            origin.push(local_branch.name, set_upstream=True)
        else:
            if repo.active_branch.name == badge_branch:
                local_branch = repo.heads[badge_branch]
                origin.push(badge_branch, set_upstream=True)
            else:
                if badge_branch in [head.name for head in repo.heads]:
                    local_branch = repo.heads[badge_branch]
                    origin.push(badge_branch, set_upstream=True)
                else:
                    local_branch = repo.create_head(badge_branch, default_branch)
                    origin.push(local_branch.name, set_upstream=True)

        return local_branch.checkout()

    except Exception as e:
        print(f'Error: {e}')
        return None


def check_user_inputs(available_badge_styles, badge_style, label_color, message_color):
    """
    Check user inputs

    Parameter(s):
    available_badge_styles: a list of available badge styles
    badge_style           : badge appearance
    label_color           : badge background hex color (left side)
    message_color         : badge background hex color (right side)

    Return: boolean
    """
    if all([
            check_hex_color(label_color),
            check_hex_color(message_color),
            badge_style in available_badge_styles
            ]):
        return True
    else:
        return False


def check_hex_color(hex_color):
    """
    Check if the hex color variable is valid

    Parameter(s):
    hex_color: hex color on label or message

    Return: boolean
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) not in [3, 6]:
        return False
    try:
        int(hex_color, 16)
        return True
    except ValueError:
        return False


def create_badge_dict(badge_style, label, label_color, message, message_color):
    """
    Create python dictionary object for badge json processing

    Parameter(s):
    badge_style  : badge appearance
    label        : badge text (left side)
    label_color  : badge background hex color (left side)
    message      : badge text (right side)
    message_color: badge background hex color (right side)

    Return: python dictionary object
    """
    badge_dict = {}
    badge_dict.update(TPL_STYLE=badge_style, TPL_LABEL=label, TPL_LCOLOR=label_color,
                      TPL_MESSAGE=message, TPL_COLOR=message_color)
    return badge_dict


def create_badge_json(badge_file_src, badge_dict, badge_name):
    """
    Create badge json files

    Parameter(s):
    badge_dict: a python dictionary for shields.io endpoint badge
    badge_name: badge name (e.g. badge)

    Return: boolean
    """
    badge_file_dst = f'badges/{badge_name}.json'

    try:
        with open(badge_file_src, 'r') as file:
            file_content = file.read()

        for tpl_string, new_string in badge_dict.items():
            file_content = file_content.replace(tpl_string, new_string)

        with open(badge_file_dst, 'w') as file:
            file.write(file_content)
        return True

    except FileNotFoundError:
        print(f"Error: File '{badge_file_src}' not found.")
        return False
    except Exception as e:
        print(f"Error: Failed to create file - {e}")
        return False


def check_badge_changes(repo, badge_name):
    """
    Check if there are badge changes

    Parameter(s):
    repo: repo class object 'git.repo.base.Repo'

    Return: boolean
    """
    if any([
            f'badges/{badge_name}.json' in repo.untracked_files,
            len(repo.git.diff('HEAD', f'badges/{badge_name}.json')) > 0,
            ]):
        return True
    else:
        return False  # pragma: no cover


def push_changes(repo, remote_name, badge_branch, badge_name, gitconfig_name, gitconfig_email, msg_suffix):
    """
    Ensure git config is set, then push commits to remote

    Parameter(s):
    repo           : repo class object 'git.repo.base.Repo'
    remote_name    : remote name (e.g. origin)
    badge_branch   : badge branch name (e.g. badges)
    badge_name     : badge name (e.g. badge)
    gitconfig_name : git config user name
    gitconfig_email: git config user email

    Return: commit hash or None
    """
    try:
        reader = repo.config_reader()
        name = reader.get_value("user", "name", default=gitconfig_name)
        email = reader.get_value("user", "email", default=gitconfig_email)

        if not all([name, email]):
            with repo.config_writer() as writer:
                writer.set_value("user", "name", gitconfig_name)
                writer.set_value("user", "email", gitconfig_email)
                writer.set_value('pull', 'rebase', 'false')

        repo.index.add([f'badges/{badge_name}.json'])
        repo.index.write()
        message = f'add/update to branch ({badge_branch}) {msg_suffix}'
        commit = repo.index.commit(message)
        commit_hash = f'{commit.hexsha}'

        repo.git.push("--set-upstream", remote_name, badge_branch)
        return commit_hash

    except Exception as e:
        print(f'Error: {e}\n')
        return None


def create_shieldsio_endpoint_badge(repo, badge_branch, badge_name):
    """
    Create Shields.io Endpoint Badge

    Parameter(s):
    repo        : repo class object 'git.repo.base.Repo'
    badge_name  : badge name (e.g. badge)
    badge_branch: badge branch name (e.g. badges)

    Return: Shields.io endpoint badge
    """
    shields_io = 'https://img.shields.io/endpoint'
    raw_github = 'https://raw.githubusercontent.com'
    repo_remotes_url = repo.remotes.origin.url
    owner_repo = '/'.join(repo_remotes_url.rsplit('/', 2)[-2:]).replace('.git', '').replace('git@github.com:', '')
    eb = f'![{badge_name}]({shields_io}?url={raw_github}/{owner_repo}/refs/heads/{badge_branch}/badges/{badge_name}.json)'

    return eb


def cicleanup(repo, remote_name, default_branch, badge_branch):
    """
    pytest Cleanup

    Parameter(s):
    repo          : repo class object 'git.repo.base.Repo'
    remote_name   : remote name (e.g. origin)
    badge_branch  : badge branch name (e.g. badges)
    default_branch: default branch of the repo
    """
    print(f'🗑️ Cleanup starts - switch to default branch ({default_branch}) and remove test branch ({badge_branch})')
    try:
        # delete local CI-Testing branch
        repo.heads[f'{default_branch}'].checkout()
        repo.delete_head(badge_branch)
        print(f'✅ Delete local working branch ({badge_branch}) successfully')

        # delete remote CI-Testing branch
        origin = repo.remote(remote_name)
        origin.push(refspec=f':{badge_branch}')
        print(f'✅ Delete remote working branch ({badge_branch}) successfully\n')

        return True

    except Exception as e:
        print(f'❌ Error: Cleanup failed - {e}\n')
        return False


@click.command()
@click.option('--badge-name', default='badge', help='default: badge')
@click.option('--badge-file-src', default='src/pkg_18604/default/template.json', help='default: src/pkg_18604/default/template.json')  # noqa: E501
@click.option('--badge-branch', default='badges', help='default: badges')
@click.option('--remote-name', default='origin', help='default: origin')
@click.option('--badge-style', default='flat', help='default: flat (flat, flat-square, plastic, for-the-badge, social)')  # noqa: E501
@click.option('--label', default='demo', help='default: demo (badge left side text)')
@click.option('--label-color', default='2e2e2e', help='default: 2e2e2e (badge left side hex color)')
@click.option('--message', default='no status', help='default: no status (badge right side text)')
@click.option('--message-color', default='2986CC', help='default: 2986CC (badge right side hex color)')
@click.option('--gitconfig-name', default='Mona Lisa', help='default: Mona Lisa')
@click.option('--gitconfig-email', default='mona.lisa@example.com', help='default: mona.lisa@example.com')
@click.option('--ci-cleanup', default=False, help='default: False')
@click.version_option(version=__version__)
def main(badge_branch, badge_name, remote_name, badge_style, label, label_color, message, message_color, badge_file_src, gitconfig_name, gitconfig_email, ci_cleanup):  # noqa: E501
    repo = get_repo()
    available_badge_styles = ['flat', 'flat-square', 'plastic', 'for-the-badge', 'social']
    default_branch = repo.git.execute(['git', 'rev-parse', '--abbrev-ref', f'{remote_name}/HEAD']).lstrip('origin/')

    msg_suffix = ''
    if 'COVERAGE_RUN' in os.environ:
        msg_suffix = '[CI - Testing]'

    print(f'🚀 Starting to create a badge ({badge_name}.json) on branch ({badge_branch})\n')
    if checkout_branch(repo, remote_name, default_branch, badge_branch) is None:
        print(f'❌ failed to checkout {badge_branch}\n')

    else:
        print(f'✅ checkout branch ({badge_branch}) locally')
        if check_user_inputs(available_badge_styles, badge_style, label_color, message_color):
            print('✅ validated inputs from command line options')

            badge_dict = create_badge_dict(badge_style, label, label_color, message, message_color)
            if create_badge_json(badge_file_src, badge_dict, badge_name):
                print(f'✅ created {badge_name}.json from template.json')

                if check_badge_changes(repo, badge_name):
                    print(f'✅ found unstaged changes ready to stage, commit, and push to {remote_name}')

                    commit_hash = push_changes(repo, remote_name, badge_branch, badge_name, gitconfig_name, gitconfig_email, msg_suffix)  # noqa: E501
                    if commit_hash is not None:
                        print(f'✅ pushed commit ({commit_hash[:7]}) to remote with branch ({badge_branch})')

                        endpoint_badge = create_shieldsio_endpoint_badge(repo, badge_branch, badge_name)
                        print(f'\n🎉 Endpoint Badge: {endpoint_badge}\n')

                    else:
                        print(f'❌ failed to push changes to {remote_name}')
                else:
                    print('✅ found no changes (current is up to date)')
            else:
                print(f'❌ failed to create {badge_name}.json')
        else:
            print('❌ one or more of your inputs failed validations')

        # CI-Cleanup
        if ci_cleanup:
            cicleanup(repo, remote_name, default_branch, badge_branch)


if __name__ == '__main__':  # pragma: no cover
    main()
