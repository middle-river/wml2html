#!/usr/bin/python3

import collections
import re
import sys


HTML = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta content="text/html; charset=UTF-8" http-equiv="content-type">
<title>%(title)s</title>
%(script)s
</head>
<body>
<h1>%(title)s</h1>
%(subtitle)s
<hr>
%(body)s
<hr>
<div><a href="../">[Back]</a></div>
<address>
%(changelog)s
%(author)s
</address>
</body>
</html>"""

BLOCK1_TAG = set('=12345-+*|&')
BLOCK2_TAG = set('!^"@')
INLINE_TAG = {'\\': '\\', '/': '<br>', '(': '<em>', ')': '</em>', '<': '<strong>', '>': '</strong>'}


def escape(line):
  line = line.replace('&', '&amp;')
  line = line.replace('<', '&lt;')
  line = line.replace('>', '&gt;')
  line = line.replace('"', '&quot;')
  return line


def parse_inline(line, variables):
  buf = []
  while line:
    pos = line.find('\\')
    if pos != 0:
      if pos < 0:
        pos = len(line)
      buf.append(escape(line[:pos]))
      line = line[pos:]
      continue
    assert len(line) >= 2
    if line[1] in INLINE_TAG:
      buf.append(INLINE_TAG[line[1]])
      line = line[2:]
      continue
    if line[1] == '[':
      pos1 = line.index('\\:', 2)
      pos2 = line.index('\\]', pos1 + 2)
      buf.append('<a href="%s">%s</a>' % (line[pos1 + 2:pos2], line[2:pos1]))
      line = line[pos2 + 2:]
      continue
    if line[1] == '`':
      pos1 = line.index('\\\'', 2)
      buf.append(line[2:pos1])
      line = line[pos1 + 2:]
      continue
    assert False, 'Invalid tag: %s' % line
  return ''.join(buf)


def process_block(tag, exprs, variables):
  if tag == '=':
    return '<hr>'
  if tag in '12345':
    text = ''.join([expr if isinstance(expr, str) else ''.join(expr) for expr in exprs])
    return '<h%s>%s</h%s>' % (tag, text, tag)
  if tag == '"':
    text = '\n'.join([expr if isinstance(expr, str) else '\t'.join(expr) for expr in exprs])
    return '<pre>\n%s\n</pre>' % text
  if tag == '@':
    text = ''.join([expr if isinstance(expr, str) else '\t'.join(expr) for expr in exprs])
    return '%s' % text

  if tag == '-' or tag == '+':
    exprs = sum([[expr] if isinstance(expr, str) else list(expr) for expr in exprs], [])
    html = []
    html.append('<ul>\n' if tag == '-' else '<ol>\n')
    drop_tags = False
    for expr in exprs:
      if not expr:
        drop_tags = True
        continue
      if drop_tags:
        html.append('%s\n' % expr)
        drop_tags = False
      else:
        html.append('<li>%s</li>\n' % expr)
    html.append('</ul>' if tag == '-' else '</ol>')
    return ''.join(html)
  if tag == '*':
    exprs = sum([[expr] if isinstance(expr, str) else list(expr) for expr in exprs], [])
    assert len(exprs) % 2 == 0
    html = []
    html.append('<dl>\n')
    for i, expr in enumerate(exprs):
      if i % 2 == 0:
        html.append('<dt>%s</dt>\n' % expr)
      else:
        html.append('<dd>%s</dd>\n' % expr)
    html.append('</dl>')
    return ''.join(html)
  if tag == '|':
    assert exprs
    exprs = sum([[expr] if isinstance(expr, str) else list(expr) for expr in exprs], [])
    fmt = exprs[0]
    cols = len(fmt)
    assert len(exprs[1:]) % cols == 0, '%d %% %d != 0, fmt=%s' % (len(exprs[1:]), cols, fmt)
    html = []
    html.append('<table border="1">\n')
    for i, expr in enumerate(exprs[1:]):
      align = {'l': 'left', 'c': 'center', 'r': 'right'}[fmt[i % cols]]
      if i % cols == 0:
        html.append('<tr>\n')
      html.append('<td align="%s">%s</td>\n' % (align, expr))
      if (i + 1) % cols == 0:
        html.append('</tr>\n')
    html.append('</table>')
    return ''.join(html)
  if tag == '&':
    html = []
    add_tag = True
    for expr in exprs:
      if isinstance(expr, str):
        if not add_tag:
          html[-1] += '</p>'
          add_tag = True
        html.append(expr)
      else:
        if add_tag:
          html.append('<p>' + '\t'.join(expr))
          add_tag = False
        else:
          html.append('\t'.join(expr))
    if not add_tag:
      html[-1] += '</p>'
    return ''.join(html)
  if tag == '!':
    exprs = sum([[expr] if isinstance(expr, str) else list(expr) for expr in exprs], [])
    assert len(exprs) % 2 == 0, str(exprs)
    for i in range(0, len(exprs), 2):
      variables[exprs[i]] = exprs[i + 1]
    return ''
  if tag == '^':
    exprs = sum([[expr] if isinstance(expr, str) else list(expr) for expr in exprs], [])
    assert len(exprs) % 3 == 0
    html = []
    html.append('<div class="center">\n')
    for i in range(0, len(exprs), 3):
      html.append('<div class="figure"><a href="%s"><img class="small" src="%s">%s</a></div>\n' % (exprs[i], exprs[i + 1], exprs[i + 2]))
    html.append('</div>')
    return ''.join(html)
  assert False


def parse_block(lines, variables):
  line = lines[0]
  lines[:] = lines[1:]

  if not line:
    return ''

  if len(line) >= 2 and line[0] == '\\' and line[1] in BLOCK1_TAG:
    tag = line[1]
    exprs = []
    if len(line) == 3 and line[2] == '{':
      while True:
        assert lines
        line = lines[0]
        lines[:] = lines[1:]
        if line == '\\%s}' % tag:
          break
        if len(line) >= 2 and line[0] == '\\' and line[1] in BLOCK1_TAG | BLOCK2_TAG:
          lines[0:0] = [line]
          exprs.append(parse_block(lines, variables))
        elif line:
          exprs.append(tuple([parse_inline(expr, variables) for expr in line.split('\t')]))
        else:
          exprs.append((''))
    elif len(line) == 2 or line[2] == '\t':
      if len(line) >= 3:
        exprs.append(tuple([parse_inline(expr, variables) for expr in line[3:].split('\t')]))
    else:
      assert False, 'Invalid block1: %s' % line
    return process_block(tag, exprs, variables)

  if len(line) >= 2 and line[0] == '\\' and line[1] in BLOCK2_TAG:
    tag = line[1]
    exprs = []
    if len(line) == 3 and line[2] == '{':
      while True:
        assert lines
        line = lines[0]
        lines[:] = lines[1:]
        if line == '\\%s}' % tag:
          break
        else:
          exprs.append(tuple(line.split('\t')))
    elif len(line) == 2 or line[2] == '\t':
      if len(line) >= 3:
        exprs.append(tuple(line[3:].split('\t')))
    else:
      assert False, 'Invalid block2: %s' % line
    return process_block(tag, exprs, variables)

  html = []
  add_tag = True
  lines[0:0] = [line]
  while True:
    if not lines:
      break
    line = lines[0]
    if len(line) >= 2 and line[0] == '\\' and line[1] in BLOCK1_TAG | BLOCK2_TAG:
      break
    lines[:] = lines[1:]
    if not line:
      if not add_tag:
        html[-1] += '</p>'
      add_tag = True
      continue
    if add_tag:
      html.append('<p>' + parse_inline(line, variables))
      add_tag = False
    else:
      html.append(parse_inline(line, variables))
  if not add_tag:
    html[-1] += '</p>'
  return '\n'.join(html)


def main():
  lines = []
  for line in sys.stdin:
    lines.append(line.rstrip('\r\n'))

  body = []
  variables = collections.defaultdict(str)
  while lines:
    body.append(parse_block(lines, variables))
  body = [b for b in body if b]

  variables['body'] = '\n'.join(body)
  html = HTML % variables
  print(html)


if __name__ == '__main__':
  main()
