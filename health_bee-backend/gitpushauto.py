import os
import subprocess


def git_push(commit_message, repo_link=None):
    if not os.path.exists('.git'):
        # If there is no initial repository, prompt for commit message and create a new repository
        subprocess.run(['git', 'init'])
        subprocess.run(['git', 'add', '.'])

        # Create README.md file if it doesn't exist
        if not os.path.exists('README.md'):
            with open('README.md', 'w') as readme_file:
                readme_file.write('Initial commit')
            subprocess.run(['git', 'add', 'README.md'])

        subprocess.run(['git', 'commit', '-m', commit_message])

        # Rename the branch from master to main
        subprocess.run(['git', 'branch', '-M', 'main'])

        if repo_link is not None:
            # Add the remote repository and push changes
            subprocess.run(['git', 'remote', 'add', 'origin', repo_link])
            subprocess.run(['git', 'push', '-u', 'origin', 'main'])
    else:
        # If repository already exists, just commit the changes
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', commit_message])

        if repo_link is not None:
            # Push the changes to the repository
            subprocess.run(['git', 'remote', 'add', 'origin', repo_link])
            subprocess.run(['git', 'push', '-u', 'origin', 'main'])


# Example usage:
commit_msg = input("Enter commit message: ")
repo_url = input("Enter repository URL (leave blank if not initialized): ")

git_push(commit_msg, repo_url)
