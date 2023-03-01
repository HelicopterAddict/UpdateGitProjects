import os
import subprocess
from typing import List

GET_BRANCH_NAME: str = 'git rev-parse --abbrev-ref'
GET_CURRENT_BRANCH_NAME_ARGS: List[str] = f'{GET_BRANCH_NAME} HEAD'.split()
GET_MASTER_BRANCH_NAME_ARGS: List[str] = f'{GET_BRANCH_NAME} origin/HEAD'.split()

rootdir = os.getcwd()
print('Root directory is', rootdir)

def prompt_and_run(dialog, command):

    choice = input(dialog).lower()
    if choice == 'y':
        try:
            subprocess.check_call(command.split())
        except Exception:
            print('Something went wrong')
    else:
        print('Alright then!\n')

def is_git_repo():
    try:
        subprocess.check_call('git rev-parse --is-inside-work-tree'.split())
    except Exception:
        return False
    
    return True

def is_not_master(branch_name: str):
    return branch_name != 'main' and branch_name != 'master'

def remove_origin_from_string(string: str):
    return string.split('origin/')[1]

def clean_string(string: str) -> str:
    return str(string, 'utf-8').strip()

for folder in os.scandir():

    if not folder.is_file():
        print('\n', '*'*4, f' Checking {folder.name}', '*'*4)
        os.chdir(rootdir)
        os.chdir(folder.path)

        if is_git_repo():
            subprocess.check_call('git fetch'.split())
            subprocess.check_call('git status'.split())
            branch_name = subprocess.check_output(GET_CURRENT_BRANCH_NAME_ARGS)
            branch_name = clean_string(branch_name)

            if is_not_master(branch_name):
                master_branch = subprocess.check_output(GET_MASTER_BRANCH_NAME_ARGS)
                master_branch = clean_string(master_branch)
                master_branch_name = remove_origin_from_string(master_branch)
                choice_switch = prompt_and_run(f'\nDo you want to switch to {master_branch_name}? (y/n): ', f'git switch {master_branch_name}')

            prompt_and_run('\nDo you want to pull latest changes? (y/n): ', 'git pull')
