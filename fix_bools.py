import os, glob
files = glob.glob('templates/cotton/rdp/**/*.html', recursive=True)
for f in files:
    content = open(f, encoding='utf-8').read()
    content = content.replace('="False"', '=False')
    open(f, 'w', encoding='utf-8').write(content)
