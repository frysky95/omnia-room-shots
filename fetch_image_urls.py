#!/usr/bin/env python3
"""
Script to fetch image URLs for every image in the omnia-room-shots repository.
Generates GitHub raw URLs for all JPG files in the repository.
"""

import os
import subprocess
from urllib.parse import quote

def get_repo_info():
    """Get repository owner, name, and current branch."""
    try:
        # Get remote URL
        remote_output = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
        
        # Parse GitHub URL to extract owner and repo
        # Format: https://github.com/owner/repo.git or https://github.com/owner/repo
        if remote_output.startswith('https://github.com/'):
            parts = remote_output.replace('https://github.com/', '').replace('.git', '').split('/')
            owner = parts[0]
            repo = parts[1]
        else:
            raise ValueError(f"Unsupported remote URL format: {remote_output}")
        
        # Get current branch
        branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
        
        return owner, repo, branch
    
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to get repository information: {e}")

def find_image_files():
    """Find all JPG image files in the repository."""
    image_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                # Get relative path from repository root
                rel_path = os.path.relpath(os.path.join(root, file), '.')
                image_files.append(rel_path)
    
    return sorted(image_files)

def generate_image_urls():
    """Generate GitHub raw URLs for all image files."""
    try:
        owner, repo, branch = get_repo_info()
        print(f"Repository: {owner}/{repo}")
        print(f"Branch: {branch}")
        print(f"Base URL: https://raw.githubusercontent.com/{owner}/{repo}/{branch}/")
        print()
        
        image_files = find_image_files()
        print(f"Found {len(image_files)} image files:")
        print()
        
        urls = []
        for image_file in image_files:
            # URL encode the filename to handle special characters and spaces
            encoded_filename = quote(image_file)
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{encoded_filename}"
            urls.append(url)
            print(url)
        
        print()
        print(f"Total image URLs generated: {len(urls)}")
        
        return urls
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    generate_image_urls()