# Omnia Room Shots - Image URL Fetcher

This repository contains 570 furniture room shot images. The scripts provided here generate URLs for accessing all images in the repository via GitHub's raw content delivery.

## Generated Files

The following scripts and output files are available:

### Scripts

1. **`fetch_image_urls.py`** - Basic script that displays all image URLs
2. **`generate_image_urls.py`** - Enhanced script that creates multiple output formats

### Output Files

When you run `generate_image_urls.py`, it creates three output files:

1. **`image_urls_only.txt`** - Plain text file with one URL per line (570 URLs)
2. **`image_data.json`** - JSON format with metadata including file sizes
3. **`image_data.csv`** - CSV format suitable for spreadsheet applications

## Usage

### Basic Usage
```bash
python3 fetch_image_urls.py
```

### Generate All Output Formats
```bash
python3 generate_image_urls.py
```

## Sample URLs

All URLs follow this pattern:
```
https://raw.githubusercontent.com/frysky95/omnia-room-shots/[branch]/[filename]
```

Example URLs:
- https://raw.githubusercontent.com/frysky95/omnia-room-shots/copilot/fix-d6e281e5-9137-45c4-bbde-3dcde535f63d/AlbanySectionalRoom1.jpg
- https://raw.githubusercontent.com/frysky95/omnia-room-shots/copilot/fix-d6e281e5-9137-45c4-bbde-3dcde535f63d/Athens%20-%20Armchair_room.jpg

## Repository Information

- **Repository:** frysky95/omnia-room-shots
- **Total Images:** 570 JPG files
- **File Size Range:** ~82KB to ~761KB
- **Content:** Furniture room shots including sofas, sectionals, chairs, recliners, and other furniture pieces

## Features

- Handles special characters and spaces in filenames through URL encoding
- Provides file size information in both bytes and MB
- Supports multiple output formats for different use cases
- Automatically detects repository information from git configuration

## Requirements

- Python 3.x
- Git (for repository information detection)
- Internet access (for URL validation testing)

## File Format Support

Currently processes:
- `.jpg` files
- `.jpeg` files

The scripts automatically discover all image files in the repository and generate appropriate URLs for each one.