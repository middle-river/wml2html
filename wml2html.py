#!/usr/bin/python3

import collections
import sys

BLOCK1_TAG = set('=12345-+*|&!^')
BLOCK2_TAG = set('"@')
INLINE_TAG = {'\\': '\\', '/': '<br>', '(': '<em>', ')': '</em>', '<': '<strong>', '>': '</strong>'}

TEMPLATE = """\
<!DOCTYPE html>
<html>
%(header)s<body style="background-color: #ccccff;">
%(document)s
<hr>
<p><a href="%(home)s">[Home]</a></p>
<div align="right">
%(changelog)s%(author)s
</div>
</body>
</html>
"""

def escape(line):
  line = line.replace('&', '&amp;')
  line = line.replace('<', '&lt;')
  line = line.replace('>', '&gt;')
  line = line.replace('"', '&quot;')
  line = line.replace(':', '&#58;')
  return line

def parse_inline(line, variables, ln):
  buf = []
  while line:
    pos = line.find('\\')
    if pos != 0:
      if pos < 0:
        pos = len(line)
      buf.append(escape(line[:pos]))
      line = line[pos:]
      continue
    assert len(line) >= 2, '[%d] Invalid tag.' % ln
    if line[1] in INLINE_TAG:
      buf.append(INLINE_TAG[line[1]])
      line = line[2:]
      continue
    if line[1] == '[':
      pos1 = line.index('\\]', 2)
      assert pos1 >= 0, '[%d] The tag "[" is not closed.' % ln
      pos2 = line.find('\\:', 2, pos1)
      if pos2 < 0:
        name = escape(line[2:pos1])
        buf.append('<a id="%s" name="%s"></a>' % (name, name))
      else:
        text = escape(line[2:pos2])
        link = escape(line[pos2 + 2:pos1])
        buf.append('<a href="%s">%s</a>' % (link, text))
      line = line[pos1 + 2:]
      continue
    if line[1] == '{':
      pos1 = line.index('\\}', 2)
      assert pos1 >= 0, '[%d] The tag "{" is not closed.' % ln
      var = line[2:pos1]
      assert var in variables, '[%d] Undefined variable: %s.' % (ln, var)
      buf.append(variables[var])
      line = line[pos1 + 2:]
      continue
    if line[1] == '`':
      pos1 = line.index("\\'", 2)
      assert pos1 >= 0, '[%d] The tag "`" is not closed.' % ln
      buf.append(line[2:pos1])
      line = line[pos1 + 2:]
      continue
    assert False, '[%d] Invalid tag.' % ln
  return ''.join(buf)

def parse_paragraph(lines, variables):
  paragraph = []
  while True:
    assert lines, 'Paragraph must end with empty line before end of file.'
    line, ln = lines.pop(0)
    if not line:
      break
    paragraph.append(parse_inline(line, variables, ln))
  return '<p>%s</p>' % ''.join(paragraph)

def process_block(tag, exprs, variables, ln, global_element):
  if tag == '"':
    assert len(exprs) == 1, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    return '\n<pre style="background-color: #ccffcc">\n%s\n</pre>' % exprs[0]
  if tag == '@':
    assert len(exprs) == 1, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    return exprs[0]
  if tag == '=':
    assert len(exprs) == 0, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    return '<hr>'
  if tag in '12345':
    assert len(exprs) == 1, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    if tag == '1':
      return '<h%s align="center">%s</h%s>' % (tag, exprs[0], tag)
    else:
      return '<h%s>%s</h%s>' % (tag, exprs[0], tag)
  if tag == '-' or tag == '+':
    assert len(exprs) >= 1, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    block = ['<ul>' if tag == '-' else '<ol>']
    for expr in exprs:
      if expr[:4] in {'<ul>', '<ol>', '<dl>'}:
        block.append('%s' % expr)
      else:
        block.append('<li>%s</li>' % expr)
    block.append('</ul>' if tag == '-' else '</ol>')
    return '\n'.join(block)
  if tag == '*':
    assert exprs and len(exprs) % 2 == 0, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    block = ['<dl>']
    for i, expr in enumerate(exprs):
      if i % 2 == 0:
        block.append('<dt>%s</dt>' % expr)
      else:
        if expr[:4] in {'<ul>', '<ol>', '<dl>'}:
          block.append('%s' % expr)
        else:
          block.append('<dd>%s</dd>' % expr)
    block.append('</dl>')
    return '\n'.join(block)
  if tag == '|':
    assert exprs and (len(exprs) - 1) % len(exprs[0]) == 0, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    fmt = exprs[0]
    cols = len(fmt)
    block = ['<table%s border="1">' % (' align="center"' if global_element else '')]
    for i, expr in enumerate(exprs[1:]):
      align = {'l': 'left', 'c': 'center', 'r': 'right'}.get(fmt[i % cols], 'left')
      if i % cols == 0:
        block.append('<tr>')
      block.append('<td align="%s">%s</td>' % (align, expr))
      if (i + 1) % cols == 0:
        block.append('</tr>')
    block.append('</table>')
    return '\n'.join(block)
  if tag == '&':
    assert len(exprs) >= 1, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    return '\n'.join(['<div>'] + exprs + ['</div>'])
  if tag == '!':
    assert exprs and len(exprs) % 2 == 0, '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    for i in range(0, len(exprs), 2):
      variables[exprs[i]] = exprs[i + 1]
    return '<!-- var -->'
  if tag == '^':
    assert len(exprs) == 1 or (exprs and len(exprs) % 3 == 0), '[%d] Invalid number of parameters (%d) for the tag "%s".' % (ln, len(exprs), tag)
    if len(exprs) == 1:
      return '<div%s><img src="%s"></div>' % (' align="center"' if global_element else '', exprs[0])
    block = ['<div%s>' % (' align="center"' if global_element else '')]
    h = ' height=%s' % variables['thumbnail_height'] if 'thumbnail_height' in variables else ''
    for i in range(0, len(exprs), 3):
      block.append('<figure style="display: inline-table;"><a href="%s"><img%s src="%s" border="2"><figcaption>%s</figcaption></a></figure>' % (exprs[i], h, exprs[i + 1], exprs[i + 2]))
    block.append('</div>')
    return '\n'.join(block)
  assert False, '[%d] Unexpected tag "%s".' % (ln, tag)

def parse_block(lines, variables, global_element):
  line, ln = lines.pop(0)
  tag = line[1]
  if tag in BLOCK1_TAG:
    if len(line) == 2 or line[2] == '\t':	# Block 1 single line.
      if len(line) == 2:
        exprs = []
      else:
        exprs = [parse_inline(expr, variables, ln) for expr in line[3:].split('\t')]
    else:	# Block 1 multiple lines.
      exprs = []
      while True:
        assert lines, '[%d] The tag "%s" has no end tag.' % (ln, tag)
        if lines[0][0] == '\\%s}' % tag:
          lines.pop(0)
          break
        if check_block(lines):
          exprs.append(parse_block(lines, variables, False))
        else:
          assert lines[0][0], '[%d] Empty line exists in the tag "%s".' % (ln, tag)
          line1, ln1 = lines.pop(0)
          exprs.extend([parse_inline(expr, variables, ln1) for expr in line1.split('\t')])
  elif tag in BLOCK2_TAG:
    if len(line) == 2 or line[2] == '\t':	# Block 2 single line.
      exprs = [line[3:]]
    else:	# Block 2 multiple lines.
      exprs = []
      while True:
        assert lines, '[%d] The tag "%s" has no end tag.' % (ln, tag)
        if lines[0][0] == '\\%s}' % tag:
          lines.pop(0)
          break
        exprs.append(lines.pop(0)[0])
      exprs = ['\n'.join(exprs)]
  return process_block(tag, exprs, variables, ln, global_element)

def check_block(lines):
  line, ln = lines[0]
  if len(line) < 2 or line[0] != '\\' or line[1] not in BLOCK1_TAG | BLOCK2_TAG:
    return False
  if len(line) == 2 or line[2] == '\t':
    return True
  if len(line) == 3 and line[2] == '{':
    return True
  assert False, '[%d] Invalid block start tag: %s' % (ln, line)

def main():
  assert len(sys.argv) == 1, 'usage: %s < WML_FILE > HTML_FILE' % sys.argv[0]

  lines = [(line.rstrip('\r\n'), ln + 1) for ln, line in enumerate(sys.stdin.readlines())]

  variables = collections.defaultdict(str)
  document = []
  while lines:
    if not lines[0][0]:
      lines.pop(0)
      continue
    if check_block(lines):
      document.append(parse_block(lines, variables, True))
    else:
      document.append(parse_paragraph(lines, variables))

  variables['document'] = '\n'.join(document)
  page = TEMPLATE % variables
  print(page, end='')

if __name__ == '__main__':
  main()
