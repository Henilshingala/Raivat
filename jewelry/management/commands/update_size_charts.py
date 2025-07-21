from django.core.management.base import BaseCommand
import os
import re

class Command(BaseCommand):
    help = 'Updates all size chart files to use shared CSS'

    def handle(self, *args, **options):
        # Path to size chart directory
        size_chart_dir = os.path.join('jewelry', 'templates', 'jewelry', 'size-chart')
        
        # New content to replace the style block
        new_content = '''{% load static %}
<link rel="stylesheet" href="{% static 'jewelry/size-chart/shared-styles.css' %}">
'''

        # Regular expression to match the style block
        style_pattern = re.compile(r'<style>.*?</style>\s*', re.DOTALL)

        # Process each HTML file in the directory
        for filename in os.listdir(size_chart_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(size_chart_dir, filename)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace the style block with the new content
                new_file_content = style_pattern.sub(new_content, content)
                
                # Write the updated content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_file_content)
                
                self.stdout.write(self.style.SUCCESS(f'Successfully updated {filename}'))

        # Ensure the shared CSS file is in the correct static directory
        static_dir = os.path.join('jewelry', 'static', 'jewelry', 'size-chart')
        os.makedirs(static_dir, exist_ok=True)
        
        css_source = os.path.join('jewelry', 'templates', 'jewelry', 'size-chart', 'shared-styles.css')
        css_dest = os.path.join(static_dir, 'shared-styles.css')
        
        # Copy the shared CSS file to the static directory
        if os.path.exists(css_source):
            with open(css_source, 'r', encoding='utf-8') as f:
                css_content = f.read()
            with open(css_dest, 'w', encoding='utf-8') as f:
                f.write(css_content)
            self.stdout.write(self.style.SUCCESS('Successfully copied shared CSS to static directory'))
        
        self.stdout.write(self.style.SUCCESS('All size chart files have been updated successfully')) 