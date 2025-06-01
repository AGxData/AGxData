import re
import glob
import os
import urllib
import urllib.request as req

with open('agnyc.md') as f:
    base = f.read()

txt = re.compile('<!--.*?-->').sub('', base)
txt = re.compile('[\\s]+').sub(' ', txt)
ls = []
for match in re.compile('<img .*? src="(.*?)" .*?>').finditer(txt):
    ls.append(match.group(1))

for path in glob.glob('images/*'):
    os.unlink(path)

n = 0
for path in ls:
    try:
        parts = path.split('/')
        with req.urlopen(path) as response:
            res = response.read()
    except urllib.error.HTTPError as e:
        print(f'fail: {path}')
        continue
    if '.' in parts[-1]:
        out = f'images/{parts[-1]}'
    else:
        n += 1
        out = f'images/{n}.img'
    with open(out, 'wb') as f:
        f.write(res)
    base = base.replace(path, out)

with open('README.md', 'w') as f:
    f.write(base)
