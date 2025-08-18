#!/usr/bin/env python3
"""
Enhanced script to fetch image URLs for every image in the omnia-room-shots repository.
Generates multiple output formats: text list, JSON, and CSV.
"""

import os
import json
import csv
import subprocess
from urllib.parse import quote

def get_repo_info():
    """Get repository owner, name, and current branch."""
    try:
        # Get remote URL
        remote_output = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], text=True).strip()
        
        # Parse GitHub URL to extract owner and repo
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

def generate_image_data():
    """Generate comprehensive image data with URLs and metadata."""
    try:
        owner, repo, branch = get_repo_info()
        base_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/"
        
        image_files = find_image_files()
        
        # Generate image data with metadata
        image_data = []
        for image_file in image_files:
            # URL encode the filename to handle special characters and spaces
            encoded_filename = quote(image_file)
            url = f"{base_url}{encoded_filename}"
            
            # Get file stats
            file_path = os.path.join('.', image_file)
            file_stats = os.stat(file_path)
            
            image_info = {
                'filename': image_file,
                'url': url,
                'size_bytes': file_stats.st_size,
                'size_mb': round(file_stats.st_size / (1024 * 1024), 2)
            }
            image_data.append(image_info)
        
        return {
            'repository': f"{owner}/{repo}",
            'branch': branch,
            'base_url': base_url,
            'total_images': len(image_data),
            'images': image_data
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def save_outputs(data):
    """Save the image data in multiple formats."""
    if not data:
        return
    
    # Save URLs only (plain text)
    with open('image_urls_only.txt', 'w', encoding='utf-8') as f:
        for image in data['images']:
            f.write(f"{image['url']}\n")
    
    # Save complete data as JSON
    with open('image_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Save as CSV
    with open('image_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'url', 'size_bytes', 'size_mb'])
        writer.writeheader()
        for image in data['images']:
            writer.writerow(image)
    
    print(f"Generated files:")
    print(f"- image_urls_only.txt: {len(data['images'])} URLs")
    print(f"- image_data.json: Complete data with metadata")
    print(f"- image_data.csv: Spreadsheet-compatible format")

def main():
    """Main function to generate and display image URLs."""
    data = generate_image_data()
    if not data:
        return
    
    print(f"Repository: {data['repository']}")
    print(f"Branch: {data['branch']}")
    print(f"Base URL: {data['base_url']}")
    print(f"Total images found: {data['total_images']}")
    print()
    
    # Display first few URLs as examples
    print("Sample URLs:")
    for i, image in enumerate(data['images'][:5]):
        print(f"{i+1}. {image['url']}")
    
    if len(data['images']) > 5:
        print(f"... and {len(data['images']) - 5} more URLs")
    
    print()
    
    # Save output files
    save_outputs(data)

if __name__ == "__main__":
    main()