#!/usr/bin/env python3
import json
import os
import requests
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from urllib.parse import urlparse
import re
import time

class PreviewLinkChecker:
    def __init__(self, base_dir: Path, languages: Optional[List[str]] = None, max_retries: int = 3, retry_delay: float = 1.0):
        self.base_dir = base_dir
        self.languages = languages
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.service_patterns = {
            'apple_music': r'audio-ssl\.itunes\.apple\.com',
            'deezer': r'cdnt-preview\.dzcdn\.net',
            'spotify': r'p\.scdn\.co'
        }
        
    def detect_service(self, url: str) -> str:
        """Detect which streaming service the preview URL belongs to."""
        domain = urlparse(url).netloc
        for service, pattern in self.service_patterns.items():
            if re.search(pattern, domain):
                return service
        return 'unknown'

    def check_preview_link(self, url: str) -> Tuple[str, bool, str, str]:
        """Check if a preview link is accessible with service-specific handling and retries."""
        service = self.detect_service(url)
        
        for attempt in range(self.max_retries):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                if service == 'apple_music':
                    response = requests.head(url, headers=headers, timeout=10)
                else:
                    headers['Range'] = 'bytes=0-1024'
                    response = requests.get(url, headers=headers, timeout=10)

                is_valid = response.status_code in [200, 206]
                if is_valid:
                    return service, True, "", response.headers.get('Content-Type', 'unknown')
                
                error = f"Status code: {response.status_code}"
                if attempt < self.max_retries - 1:
                    print(f"Retry {attempt + 1}/{self.max_retries} for {url} - {error}")
                    time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                    
                return service, False, error, response.headers.get('Content-Type', 'unknown')
                
            except requests.RequestException as e:
                error = str(e)
                if attempt < self.max_retries - 1:
                    print(f"Retry {attempt + 1}/{self.max_retries} for {url} - {error}")
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return service, False, error, 'unknown'
        
        return service, False, "Max retries exceeded", 'unknown'

    def process_file(self, file_path: str) -> List[Tuple[str, str, str, str, bool, str, str, str]]:
        """Process a single JSON file and check all preview links."""
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for entry in data:
                if 'preview_link' in entry and entry['preview_link']:
                    artist = entry.get('artist', 'Unknown Artist')
                    album = entry.get('album', 'Unknown Album')
                    url = entry['preview_link']
                    service, is_valid, error, content_type = self.check_preview_link(url)
                    # Add file_path to results
                    relative_path = os.path.relpath(file_path, self.base_dir.parent.parent)
                    results.append((artist, album, url, service, is_valid, error, content_type, relative_path))
                    
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
        return results

    def generate_html_report(self, all_results: List[Tuple[str, str, str, str, bool, str, str, str]], output_path: str):
        """Generate an HTML report with the results."""
        css = """
            body {font-family: Arial, sans-serif; margin: 20px;}
            .summary {background: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 20px;}
            .error-entry {border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;}
            .error-entry:hover {background: #f9f9f9;}
            .service-tag {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 12px;
                margin-right: 10px;
            }
            .file-path {
                color: #666;
                font-family: monospace;
                background: #f0f0f0;
                padding: 2px 5px;
                border-radius: 3px;
            }
            .apple_music {background: #fe2d55; color: white;}
            .deezer {background: #00c7f2; color: white;}
            .spotify {background: #1db954; color: white;}
            .unknown {background: #gray; color: white;}
            .timestamp {color: #666; font-size: 0.9em;}
            .retry-info {margin-top: 10px; color: #666; font-style: italic;}
        """

        # Calculate statistics
        total_links = len(all_results)
        invalid_links = [r for r in all_results if not r[4]]  # r[4] is is_valid
        service_counts = {}
        for r in all_results:
            service = r[3]  # r[3] is service
            service_counts[service] = service_counts.get(service, 0) + 1

        # Generate service statistics HTML
        service_stats = "<ul>"
        for service, count in service_counts.items():
            service_stats += f'<li><span class="service-tag {service}">{service}</span>: {count} links</li>'
        service_stats += "</ul>"

        # Generate error entries HTML
        error_entries = ""
        for artist, album, url, service, is_valid, error, content_type, file_path in invalid_links:
            error_entries += f"""
                <div class="error-entry">
                    <span class="service-tag {service}">{service}</span>
                    <strong>Artist:</strong> {artist}<br>
                    <strong>Album:</strong> {album}<br>
                    <strong>URL:</strong> <a href="{url}" target="_blank">{url}</a><br>
                    <strong>Error:</strong> {error}<br>
                    <strong>Content-Type:</strong> {content_type}<br>
                    <strong>File:</strong> <span class="file-path">{file_path}</span>
                </div>
            """

        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Preview Link Check Report</title>
            <style>{css}</style>
        </head>
        <body>
            <h1>Preview Link Check Report</h1>
            <p class="timestamp">Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>Total links checked: {total_links}</p>
                <p>Accessible links: {total_links - len(invalid_links)}</p>
                <p>Inaccessible links: {len(invalid_links)}</p>
                <p class="retry-info">Links were checked with {self.max_retries} retry attempts and {self.retry_delay}s initial delay (with exponential backoff)</p>
            </div>

            <h2>Service Distribution</h2>
            <div class="summary">
                {service_stats}
            </div>

            <h2>Invalid or Inaccessible Links</h2>
            {error_entries}
        </body>
        </html>
        """

        # Write HTML report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def run(self):
        """Run the link checker on all JSON files."""
        json_files = []
        
        # Find all JSON files in specified languages
        for lang_dir in self.base_dir.iterdir():
            if lang_dir.is_dir():
                if self.languages is None or lang_dir.name in self.languages:
                    json_files.extend(lang_dir.glob('*.json'))

        # Process all files using a thread pool
        all_results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_file = {executor.submit(self.process_file, str(file_path)): file_path 
                            for file_path in json_files}
            
            for future in future_to_file:
                file_path = future_to_file[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                    print(f"Processed {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        # Generate HTML report
        report_path = self.base_dir.parent.parent / 'reports' / f'preview_link_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        report_path.parent.mkdir(exist_ok=True)
        self.generate_html_report(all_results, str(report_path))
        print(f"\nReport generated at: {report_path}")

def main():
    parser = argparse.ArgumentParser(description='Check preview links in genre JSON files')
    parser.add_argument('--languages', nargs='+', help='Specific language codes to check (e.g., en de fr)')
    parser.add_argument('--retries', type=int, default=3, help='Number of retry attempts for failed requests')
    parser.add_argument('--retry-delay', type=float, default=1.0, help='Initial delay between retries in seconds')
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent / 'app' / 'json' / 'genres'
    checker = PreviewLinkChecker(base_dir, args.languages, args.retries, args.retry_delay)
    checker.run()

if __name__ == "__main__":
    main()
