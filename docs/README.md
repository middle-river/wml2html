<!DOCTYPE html>
<html>
<body style="background-color: #ccccff;">
<!-- var -->
<p><a id="lang_en" name="lang_en"></a>[English] <a href="#lang_ja">[日本語]</a></p>
<h1 align="center">Own Markup Language for Web Pages</h1>
<h2>Introduction</h2>
<p>I have used HTML editors such as KompoZer and BlueGriffon to create my website. They were useful tools which allow to edit in WYSIWYG or directly edit HTML, but they were not very convenient because they sometimes insert unnecessary tags or spaces, and output files with invalid HTML syntax. I usually use bare text editors and am used to TeX, so it was not efficient for me to use WYSIWYG editors or write HTML directly. Therefore, I decided to create web pages by generating HTML from files written in a simple a markup language.</p>
<p>There are various markup languages for writing documents, and one of the major ones is Markdown. Markdown has the advantage of being relatively easy to read when viewed as a text file, but the grammar is not defined as a context-free grammar as in programming languages. It is sometimes difficult to predict the outputs for complicated nested structures and character escaping. I looked into other existing lightweight markup languages but found nothing suitable for my purposes, so I made my own markup language and created a converter to HTML. The markup language was designed by ignoring the look of source text as a text file but focusing on the simplicity of the syntax.</p>
<h2>Syntax and Examples</h2>
<h3>Summary</h3>
<p>All markup tags are represented by the symbol \ and a single character, like \x. There are two types of markup tags&#58; inline elements and block elements. Inline elements can be used anywhere in a document. Block elements can be written on a single line by placing a tab character immediately after \x, or on multiple lines by using start and end tags with braces like \x{ ... \x}. When writing block elements on multiple lines, multiple inner elements can be written on each line by separating a tab character. There are two types of block elements&#58; normal block elements and meta block elements. Normal blocks have marked-up documents inside them, while meta blocks have raw HTML documents and HTML tags are not escaped.</p>
<p>A paragraph consists of consecutive lines and ends with a blank line. Consecutive lines are concatenated by replacing newlines with the variable named paragraph_newline. Its default value is a space, which will work for English. An empty string can be set to the variable for Japanese in order not to generate unnecessary whitespaces.</p>
<h3>Tag List</h3>
<table align="center" border="1">
<tr>
<td align="center"><strong>Normal Block Elements</strong></td>
<td align="left"></td>
</tr>
<tr>
<td align="center">\=</td>
<td align="left">Horizontal rule</td>
</tr>
<tr>
<td align="center">\1-\5</td>
<td align="left">H1 to H5 headings</td>
</tr>
<tr>
<td align="center">\-</td>
<td align="left">Unordered list</td>
</tr>
<tr>
<td align="center">\+</td>
<td align="left">Ordered list</td>
</tr>
<tr>
<td align="center">\*</td>
<td align="left">Description list</td>
</tr>
<tr>
<td align="center">\|</td>
<td align="left">Table</td>
</tr>
<tr>
<td align="center">\&amp;</td>
<td align="left">Block grouping</td>
</tr>
<tr>
<td align="center">\!</td>
<td align="left">Defining variables</td>
</tr>
<tr>
<td align="center">\^</td>
<td align="left">Image</td>
</tr>
<tr>
<td align="center"><strong>Meta Block Elements</strong></td>
<td align="left"></td>
</tr>
<tr>
<td align="center">\&quot;</td>
<td align="left">Preformatted text</td>
</tr>
<tr>
<td align="center">\@</td>
<td align="left">Raw HTML</td>
</tr>
<tr>
<td align="center"><strong>Inline Elements</strong></td>
<td align="left"></td>
</tr>
<tr>
<td align="center">\\</td>
<td align="left">\ symbol</td>
</tr>
<tr>
<td align="center">\/</td>
<td align="left">Line break</td>
</tr>
<tr>
<td align="center">\(text\)</td>
<td align="left">Italics</td>
</tr>
<tr>
<td align="center">\&lt;text\&gt;</td>
<td align="left">Bold</td>
</tr>
<tr>
<td align="center">\[label\]</td>
<td align="left">Label for hyperlink</td>
</tr>
<tr>
<td align="center">\[link-text\&#58;link-destination\]</td>
<td align="left">Hyperlink</td>
</tr>
<tr>
<td align="center">\{variable\}</td>
<td align="left">Referring a variable</td>
</tr>
<tr>
<td align="center">\`raw-html\'</td>
<td align="left">Raw HTML</td>
</tr>
</table>
<h3>Internal Variables</h3>
<p>This markup language allows to define variables and refer their values. The following variables are used in the script when outputting HTML.</p>
<table align="center" border="1">
<tr>
<td align="center">author</td>
<td align="left">Author name</td>
</tr>
<tr>
<td align="center">changelog</td>
<td align="left">Edit history of the page</td>
</tr>
<tr>
<td align="center">home</td>
<td align="left">URL of homepage</td>
</tr>
<tr>
<td align="center">thumbnail_height</td>
<td align="left">Height of image thumbnails</td>
</tr>
<tr>
<td align="center">paragraph_newline</td>
<td align="left">String to replace newlines in paragraphs</td>
</tr>
</table>
<h3>Syntax in BNF</h3>

<pre style="background-color: #ccffcc">
&lt;document&gt;    ::=	{ LF | &lt;block_expr&gt; | &lt;paragraph&gt; }
&lt;paragraph&gt;   ::=	&lt;inline_expr&gt; LF { &lt;inline_expr&gt; LF } LF	<i>; Paragraph</i>
&lt;block_expr&gt;  ::=	&lt;block1_tag&gt; { TAB &lt;inline_expr&gt; } LF |	<i>; Normal block on a single line</i>
			&lt;block1_tag&gt; "{" LF { &lt;block_expr&gt; | &lt;inline_expr&gt; { TAB &lt;inline_expr&gt; } LF } &lt;block1_tag&gt; "}" LF |	<i>; Normal block on multiple lines</i>
			&lt;block2_tag&gt; { TAB &lt;raw_expr&gt; } LF |	<i>; Meta block on a single line</i>
			&lt;block2_tag&gt; "{" LF { &lt;raw_expr&gt; LF } &lt;block2_tag&gt; "}" LF	<i>; Meta block on multiple lines</i>
&lt;block1_tag&gt;  ::=	"\=" | "\1" | "\2" | "\3" | "\4" | "\5" | "\-" | "\+" | "\*" | "\|" | "\&amp;" | "\!" | "\^"
&lt;block2_tag&gt;  ::=	'\"' | "\@"
&lt;inline_expr&gt; ::=	{ &lt;inline_elem&gt; }
&lt;inline_elem&gt; ::=	&lt;raw_expr&gt; |
			"\\" | "\/" | "\(" | "\)" | "\&lt;" | "\&gt;" |
			"\[" &lt;raw_expr&gt; "\]" | "\[" &lt;raw_expr&gt; "\:" &lt;raw_expr&gt; "\]" |
			"\{" &lt;raw_expr&gt; "\}" |
			"\`" &lt;raw_expr&gt; "\'"
&lt;raw_expr&gt;    ::=	&lt;String of any characters&gt;
</pre>
<h3>Description of Tags</h3>
<dl>
<dt><strong>Inline Elements</strong></dt>
<dd><div>
<em>Input</em>

<pre style="background-color: #ccffcc">
\\ symbol is used\/in \(various\) \&lt;places\&gt;. This is a \[hyperlink\:sample.png\] and a \[label\]label. \`a&lt;sup&gt;b&lt;/sup&gt;&lt;sub&gt;c&lt;/sub&gt;\'
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
\ symbol is used<br>in <em>various</em> <strong>places</strong>. This is a <a href="sample.png">hyperlink</a> and a <a id="label" name="label"></a>label. a<sup>b</sup><sub>c</sub>
</blockquote>
</div></dd>
<dt><strong>\=</strong> (Horizontal rule)</dt>
<dd><div>
Insert a horizontal rule.<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
Text 1
\=
Text 2
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
Text 1
<hr>
Text 2
</blockquote>
</div></dd>
<dt><strong>\1-\5</strong> (H1-H5 Headings)</dt>
<dd><div>
Headings corresponding to HTML tags H1-H5 are generated.<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
\2	This is
\3{
a test
\3}
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
<h2>This is </h2>
<h3>a test</h3>
</blockquote>
</div></dd>
<dt><strong>\-, \+</strong> (Unordered List and Ordered List)</dt>
<dd><div>
An unordered list or ordered list are generated.
This block has multiple elements separated by tab characters or newlines.<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
\-	a	b
\+{
AA
\-{
aa
bb
\-}
BB	CC
\+}
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
<ul>
<li>a</li>
<li>b</li>
</ul>
<ol>
<li>AA</li>
<ul>
<li>aa</li>
<li>bb</li>
</ul>
<li>BB</li>
<li>CC</li>
</ol>
</blockquote>
</div></dd>
<dt><strong>\*</strong> (Description List)</dt>
<dd><div>
A description list is generated.
This block has elements separated by tab characters or newlines, and the number of elements must be a multiple of two.
The headings and contents of each item in the list alternate.<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
\*{
a	aa
b	bb
c
cc	d	dd
\*}
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
<dl>
<dt>a</dt>
<dd>aa</dd>
<dt>b</dt>
<dd>bb</dd>
<dt>c</dt>
<dd>cc</dd>
<dt>d</dt>
<dd>dd</dd>
</dl>
</blockquote>
</div></dd>
<dt><strong>\|</strong> (Table)</dt>
<dd><div>
A table is generated.
This block has elements separated by tab characters or newlines, and the number of elements must be equal to (1 + number_of_rows * number_of_columns).
The first element is a string with the same length as the number of columns, and consists of the characters l, c and r which specifies the format of each column in the table (left-aligned, centered, or right-aligned, respectively).<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
\|{
lcr
aaa	bbb	ccc
d
e
f
\|}
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
<table border="1">
<tr>
<td align="left">aaa</td>
<td align="center">bbb</td>
<td align="right">ccc</td>
</tr>
<tr>
<td align="left">d</td>
<td align="center">e</td>
<td align="right">f</td>
</tr>
</table>
</blockquote>
</div></dd>
<dt><strong>\&amp;</strong> (Block Grouping)</dt>
<dd><div>
Combines multiple blocks into one block.
This is used when multiple blocks need to be included in a list or table.<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
\-{
\|	c	a
\&{
\|	c	b
\^	sample.png
\&}
\&{
\|	c	c
\|	c	d
\&}
\-}
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
<ul>
<li><table border="1">
<tr>
<td align="center">a</td>
</tr>
</table></li>
<li><div>
<table border="1">
<tr>
<td align="center">b</td>
</tr>
</table>
<div><img src="sample.png"></div>
</div></li>
<li><div>
<table border="1">
<tr>
<td align="center">c</td>
</tr>
</table>
<table border="1">
<tr>
<td align="center">d</td>
</tr>
</table>
</div></li>
</ul>
</blockquote>
</div></dd>
<dt><strong>\!</strong> (Defining Variables)</dt>
<dd><div>
Variable are defined.
This block has multiple elements separated by tab characters or newlines, and the number of elements must be a multiple of 2.
Variable names and variable values alternate.<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
\!{
x	123
\!}
x=\{x\}
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
<!-- var -->
x=123
</blockquote>
</div></dd>
<dt><strong>\^</strong> (Image)</dt>
<dd><div>
Images are generated.
This block has one or more elements separated by tab characters or newlines.
If there is just one element, the image is centered and displayed.
If the number of elements is a multiple of three, each of them respectively means a link destination, a thumbnail image, and a caption, and images with links and labels are displayed in a row.
<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
\^{
sample.png	sample.png	Label 1
../	sample.png	Label 2
\^}
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">
<div>
<figure style="display: inline-table;"><a href="sample.png"><img height=200 src="sample.png" border="2"><figcaption>Label 1</figcaption></a></figure>
<figure style="display: inline-table;"><a href="../"><img height=200 src="sample.png" border="2"><figcaption>Label 2</figcaption></a></figure>
</div>
</blockquote>
</div></dd>
<dt><strong>\&quot;</strong> (Preformatted Text)</dt>
<dd><div>
Preformatted text is displayed.<br><br>
<em>Input</em>

<pre style="background-color: #ccffcc">
\"{
ab\(c\)
de&lt;i&gt;f&lt;/i&gt;
\"} 
</pre>
<em>Output</em>
<blockquote style="background-color: #ccffcc;">

<pre style="background-color: #ccffcc">
ab\(c\)
de<i>f</i>
</pre>
</blockquote>
</div></dd>
<dt><strong>\@</strong> (Raw HTML)</dt>
<dd><div>
Raw HTML can be written.
</div></dd>
</dl>
<h2>Converter to HTML</h2>
<p>I wrote a converter in Python based on recursive descent parsing for generating HTML files from this web markup language. The script is available <a href="https&#58;//github.com/middle-river/wml2html">here</a>.</p>
<h2>Example</h2>
<p>I have used this markup language to create my web pages for about seven months, and it has saved my time by allowing easier writing of web pages using a text editor. The conversion script always outputs valid HTML files, and I no longer suffer from pages with invalid HTML syntax. As an example, <a href="README.wml">here</a> is the markup file used for generating this page. This markup language has only minimum functions I need, but I will use raw HTML or add new features if I come to think they are necessary.</p>
<h2>Generating README.md for GitHub</h2>
<p>(Added on 2025/01) I decided to migrate some of the contents from the current web hosting service to GitHub. For the migration, the conversion script was modified to generate README.md for GitHub. README.md for GitHub is usually written in Markdown, but Markdown is inconvenient because it does not have a strict syntax, so I decided to generate limited HTML that can be used in README.md for GitHub. The HTML that can be used in GitHub is described in <a href="https&#58;//github.github.com/gfm/">GitHub Flavored Markdown Spec</a>. For example, the <em>align</em> attribute is used since the <em>style</em> attribute is unavailable, colons (&#58;) are replaced with the numeric character reference (&amp;#58) to avoid linkification for URLs starting with http&#58;//, a blank line is inserted before the &lt;pre&gt; tag to prevent the HTML block from being interrupted. However, there are limitations such that the &lt;figcaption&gt; tag is not supported so image captions are not displayed properly.</p>
<hr>
<!-- var -->
<p><a href="#lang_en">[English]</a> <a id="lang_ja" name="lang_ja"></a>[日本語]</p>
<h1 align="center">自作のWebページ用マークアップ言語</h1>
<h2>はじめに</h2>
<p>これまで自分のホームページを作成するのに、KompoZerやBlueGriffon等のHTMLエディターを使ってきました。WYSIWYGで編集することも、HTMLを直に編集することもできて便利なツールでしたが、不要なタグや空白が勝手に挿入されたり、HTML構文が不正なファイルが出力されることもあったりと使い勝手がいまいちでした。普段はテキストエディターしか使わずTeXなどに慣れているので、WYSIWYGやHTMLタグ直書きだとWebページ作成の効率が上がりませんでした。そこで、今後はできるだけシンプルなマークアップ言語で書いたファイルからHTMLページを生成してWebページを作成することにしました。</p>
<p>文書作成用のマークアップ言語は色々ありますが、現在メジャーなものの一つにMarkdownがあります。Markdownはテキストファイルとして見た場合に比較的可読性が高いという利点がありますが、プログラミング言語のように文脈自由文法で文法が定義されておらずトークンの位置情報が意味を持つなど気持ちが悪い部分があります。リストの中に別のリストやテーブルが入るような入れ子構造や、どのような場合に文字がエスケープされるのかといった文法が明確になっていないと混乱することがあります。既存の他の軽量マークアップ言語も調べましたが自分の目的にあった適当なものがないので、独自のマークアップ言語を定義してHTMLへのコンバータを作ることにしました。テキストファイルでの見栄えは重視しませんが、できるだけシンプルな構文を持ちHTMLを直書きするよりも簡潔に表現できるようにしました。要するに自分にとっての使いやすさを第一に考えて作っています。</p>
<h2>文法と例</h2>
<h3>概要</h3>
<p>すべてのマークアップ用タグは\xのように\記号と1つの文字で表現されます。マークアップ用のタグにはインライン要素とブロック要素があります。インライン要素は文書中のどの位置でも使えます。ブロック要素は\x{...\x}のように波括弧を付けた開始タグと終了タグで範囲を囲んで複数行に書く方法と、\xの直後にタブ文字を置いて1行に書く方法とがあります。テーブルなどのブロックの要素を複数行に書く場合でも、タブで区切ることで1行の中に複数の要素を記述できます。ブロック要素には通常ブロック要素とメタブロック要素があります。通常ブロックはその内部にマークアップされた文書を持ちますが、メタブロックは生のHTML文書を持ちHTMLタグなどはエスケープされません。</p>
<p>パラグラフは、連続する行で構成されて空行で終了します。連続した行の改行はparagraph_newlineという変数に定義された文字列で置き換えられますが、その値はデフォルトではスペースです。そのため日本語の場合はこの変数を空文字にすることで、段落中の改行により不要な空白が入らないようにできます。</p>
<h3>タグ一覧</h3>
<table align="center" border="1">
<tr>
<td align="center"><strong>通常ブロック要素</strong></td>
<td align="left"></td>
</tr>
<tr>
<td align="center">\=</td>
<td align="left">水平線</td>
</tr>
<tr>
<td align="center">\1～\5</td>
<td align="left">H1～H5見出し</td>
</tr>
<tr>
<td align="center">\-</td>
<td align="left">順序無しリスト</td>
</tr>
<tr>
<td align="center">\+</td>
<td align="left">順序付きリスト</td>
</tr>
<tr>
<td align="center">\*</td>
<td align="left">記述リスト</td>
</tr>
<tr>
<td align="center">\|</td>
<td align="left">テーブル</td>
</tr>
<tr>
<td align="center">\&amp;</td>
<td align="left">ブロック連結</td>
</tr>
<tr>
<td align="center">\!</td>
<td align="left">変数定義</td>
</tr>
<tr>
<td align="center">\^</td>
<td align="left">画像</td>
</tr>
<tr>
<td align="center"><strong>メタブロック要素</strong></td>
<td align="left"></td>
</tr>
<tr>
<td align="center">\&quot;</td>
<td align="left">引用</td>
</tr>
<tr>
<td align="center">\@</td>
<td align="left">生のHTML</td>
</tr>
<tr>
<td align="center"><strong>インライン要素</strong></td>
<td align="left"></td>
</tr>
<tr>
<td align="center">\\</td>
<td align="left">\文字</td>
</tr>
<tr>
<td align="center">\/</td>
<td align="left">改行</td>
</tr>
<tr>
<td align="center">\(テキスト\)</td>
<td align="left">イタリック体</td>
</tr>
<tr>
<td align="center">\&lt;テキスト\&gt;</td>
<td align="left">ボールド体</td>
</tr>
<tr>
<td align="center">\[ラベル\]</td>
<td align="left">ページ内ラベル</td>
</tr>
<tr>
<td align="center">\[リンクテキスト\&#58;リンク先\]</td>
<td align="left">リンク</td>
</tr>
<tr>
<td align="center">\{変数名\}</td>
<td align="left">変数参照</td>
</tr>
<tr>
<td align="center">\`生HTML\'</td>
<td align="left">生のHTML</td>
</tr>
</table>
<h3>内部変数</h3>
<p>このマークアップ言語では変数を定義することができます。文書中でその値を参照することもできますが、以下の変数はスクリプト内でHTMLを出力する際に参照されます。</p>
<table align="center" border="1">
<tr>
<td align="center">author</td>
<td align="left">著者名</td>
</tr>
<tr>
<td align="center">changelog</td>
<td align="left">編集履歴</td>
</tr>
<tr>
<td align="center">home</td>
<td align="left">ホームページのURL</td>
</tr>
<tr>
<td align="center">thumbnail_height</td>
<td align="left">画像サムネイルの高さ</td>
</tr>
<tr>
<td align="center">paragraph_newline</td>
<td align="left">パラグラフ中の改行を置き換える文字列</td>
</tr>
</table>
<h3>BNFによる文法の定義</h3>

<pre style="background-color: #ccffcc">
&lt;document&gt;    ::=	{ LF | &lt;block_expr&gt; | &lt;paragraph&gt; }
&lt;paragraph&gt;   ::=	&lt;inline_expr&gt; LF { &lt;inline_expr&gt; LF } LF	<i>; 段落</i>
&lt;block_expr&gt;  ::=	&lt;block1_tag&gt; { TAB &lt;inline_expr&gt; } LF |	<i>; 通常ブロックタグの一行表記</i>
			&lt;block1_tag&gt; "{" LF { &lt;block_expr&gt; | &lt;inline_expr&gt; { TAB &lt;inline_expr&gt; } LF } &lt;block1_tag&gt; "}" LF |	<i>; 通常ブロックタグの複数行表記</i>
			&lt;block2_tag&gt; { TAB &lt;raw_expr&gt; } LF |	<i>; メタブロックタグの一行表記</i>
			&lt;block2_tag&gt; "{" LF { &lt;raw_expr&gt; LF } &lt;block2_tag&gt; "}" LF	<i>; メタブロックタグの複数行表記</i>
&lt;block1_tag&gt;  ::=	"\=" | "\1" | "\2" | "\3" | "\4" | "\5" | "\-" | "\+" | "\*" | "\|" | "\&amp;" | "\!" | "\^"
&lt;block2_tag&gt;  ::=	'\"' | "\@"
&lt;inline_expr&gt; ::=	{ &lt;inline_elem&gt; }
&lt;inline_elem&gt; ::=	&lt;raw_expr&gt; |
			"\\" | "\/" | "\(" | "\)" | "\&lt;" | "\&gt;" |
			"\[" &lt;raw_expr&gt; "\]" | "\[" &lt;raw_expr&gt; "\:" &lt;raw_expr&gt; "\]" |
			"\{" &lt;raw_expr&gt; "\}" |
			"\`" &lt;raw_expr&gt; "\'"
&lt;raw_expr&gt;    ::=	&lt;String of any characters&gt;
</pre>
<h3>タグの説明</h3>
<dl>
<dt><strong>インライン要素</strong></dt>
<dd><div>
<em>入力</em>

<pre style="background-color: #ccffcc">
\\文字が\(様々\)な\<ところ\>で\/使われます。これは\[リンク\:sample.png\]と\[label\]ラベルです。\`a&lt;sup&gt;b&lt;/sup&gt;&lt;sub&gt;c&lt;/sub&gt;\'
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
\文字が<em>様々</em>な<strong>ところ</strong>で<br>使われます。これは<a href="sample.png">リンク</a>と<a id="label" name="label"></a>ラベルです。a<sup>b</sup><sub>c</sub>
</blockquote>
</div></dd>
<dt><strong>\=</strong> (水平線)</dt>
<dd><div>
水平線を挿入します。<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
文書1
\=
文書2
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
文書1
<hr>
文書2
</blockquote>
</div></dd>
<dt><strong>\1～\5</strong> (H1～H5見出し)</dt>
<dd><div>
HTMLのH1〜H5に対応する見出しを生成します。<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
\2	これは
\3{
テストです
\3}
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
<h2>これは</h2>
<h3>テストです</h3>
</blockquote>
</div></dd>
<dt><strong>\-, \+</strong> (順序無しリスト、順序付きリスト)</dt>
<dd><div>
順序無し・順序付きリストを生成します。
このブロックはタブ文字または改行で区切られた複数の要素を持ちます。<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
\-	a	b
\+{
AA
\-{
aa
bb
\-}
BB	CC
\+}
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
<ul>
<li>a</li>
<li>b</li>
</ul>
<ol>
<li>AA</li>
<ul>
<li>aa</li>
<li>bb</li>
</ul>
<li>BB</li>
<li>CC</li>
</ol>
</blockquote>
</div></dd>
<dt><strong>\*</strong> (記述リスト)</dt>
<dd><div>
記述リストを生成します。
このブロックはタブ文字または改行で区切られた複数の要素を持ちますが、要素の数は2の倍数でなければなりません。
リストの各項目の見出しと内容が交互に並びます。<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
\*{
a	aa
b	bb
c
cc	d	dd
\*}
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
<dl>
<dt>a</dt>
<dd>aa</dd>
<dt>b</dt>
<dd>bb</dd>
<dt>c</dt>
<dd>cc</dd>
<dt>d</dt>
<dd>dd</dd>
</dl>
</blockquote>
</div></dd>
<dt><strong>\|</strong> (テーブル)</dt>
<dd><div>
テーブルを作成します。
このブロックはタブ文字または改行で区切られた複数の要素を持ちますが、要素の数は(1 + 行数 * 列数)でなければなりません。
最初の要素は、列数と同じ長さのl, c, rの3文字からなる文字列で、テーブルの各列のフォーマット(それぞれ左詰め、センタリング、右詰め)を指定します。<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
\|{
lcr
aaa	bbb	ccc
d
e
f
\|}
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
<table border="1">
<tr>
<td align="left">aaa</td>
<td align="center">bbb</td>
<td align="right">ccc</td>
</tr>
<tr>
<td align="left">d</td>
<td align="center">e</td>
<td align="right">f</td>
</tr>
</table>
</blockquote>
</div></dd>
<dt><strong>\&amp;</strong> (ブロック連結)</dt>
<dd><div>
複数のブロックを一つのブロックとしてまとめます。
リストやテーブルに複数のブロックをまとめて入れたい場合などに使います。<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
\-{
\|	c	a
\&{
\|	c	b
\^	sample.png
\&}
\&{
\|	c	c
\|	c	d
\&}
\-}
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
<ul>
<li><table border="1">
<tr>
<td align="center">a</td>
</tr>
</table></li>
<li><div>
<table border="1">
<tr>
<td align="center">b</td>
</tr>
</table>
<div><img src="sample.png"></div>
</div></li>
<li><div>
<table border="1">
<tr>
<td align="center">c</td>
</tr>
</table>
<table border="1">
<tr>
<td align="center">d</td>
</tr>
</table>
</div></li>
</ul>
</blockquote>
</div></dd>
<dt><strong>\!</strong> (変数定義)</dt>
<dd><div>
変数の値を定義します。
このブロックはタブ文字または改行で区切られた複数の要素を持ちますが、要素の数は2の倍数でなければなりません。
変数名と変数の値が交互に並びます。
HTML出力の際には、ここで定義した変数の値が使われます。<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
\!{
x	123
\!}
x=\{x\}
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
<!-- var -->
x=123
</blockquote>
</div></dd>
<dt><strong>\^</strong> (画像)</dt>
<dd><div>
画像を表示します。
このブロックはタブ文字または改行で区切られた1つ以上の要素を持ちます。
要素数が1つの場合は画像をセンタリングして表示します。
要素数が3の倍数の場合はリンク先、サムネイル画像、ラベルをそれぞれ意味し、ラベルのついたリンク付き画像を並べて表示します。
<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
\^{
sample.png	sample.png	ラベル1
../	sample.png	ラベル2
\^}
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">
<div>
<figure style="display: inline-table;"><a href="sample.png"><img height=200 src="sample.png" border="2"><figcaption>ラベル1</figcaption></a></figure>
<figure style="display: inline-table;"><a href="../"><img height=200 src="sample.png" border="2"><figcaption>ラベル2</figcaption></a></figure>
</div>
</blockquote>
</div></dd>
<dt><strong>\&quot;</strong> (引用)</dt>
<dd><div>
整形済みのテキストを表示します。<br><br>
<em>入力</em>

<pre style="background-color: #ccffcc">
\"{
ab\(c\)
de&lt;i&gt;f&lt;/i&gt;
\"} 
</pre>
<em>出力</em>
<blockquote style="background-color: #ccffcc;">

<pre style="background-color: #ccffcc">
ab\(c\)
de<i>f</i>
</pre>
</blockquote>
</div></dd>
<dt><strong>\@</strong> (生のHTML)</dt>
<dd><div>
HTMLのソースを直接記述します。
</div></dd>
</dl>
<h2>HTMLへのコンバーター</h2>
<p>Pythonで再帰下降構文解析を行い、このWebマークアップ用言語からHTMLファイルを生成するコンバーターを書きました。スクリプトは<a href="https&#58;//github.com/middle-river/wml2html">ここ</a>に置いてあります。</p>
<h2>使用例など</h2>
<p>このホームページの作成に7ヶ月ほど使用してきましたが、テキストエディターを使って手軽にWebページを用意できるようになり手間を減らすことができました。また変換スクリプトからは必ず正しいHTMLファイルが出力されるので、不正なHTML構文を持つページができることもなくなりました。参考までに、このページの生成に使われたマークアップファイルを<a href="README.wml">ここ</a>に置いておきます。このマークアップ言語には自分が必要とする最低限の機能しかありませんが、例外的な記述が必要な場合は生のHTMLを挿入して対応し、足りなくてどうしても不便な機能が出てくればその都度追加していくつもりです。</p>
<h2>GitHubのREADME.mdの生成</h2>
<p>(2025/01追記) これまで利用してきたWebホスティングサービスからコンテンツの一部をGitHubに移行することにしました。それに際して、このマークアップ言語からREADME.mdを生成することにしました。GitHubのREADME.mdはMarkdownで書かれますが、Markdownは厳格な文法を持っていないため扱いにくいので、GitHubのREADME.mdに含めることができる制限されたHTMLを生成することにしました。GitHubで扱うことができるHTMLについては、<a href="https&#58;//github.github.com/gfm/">GitHub Flavored Markdown Spec</a>に記述されています。例えば、style属性は無効になるのでalign属性を使用したり、コロン(&#58;)を実体参照(&amp;#58)に置き換えてhttp&#58;//等で始まるURLがリンク化されるのを防いだり、&lt;pre&gt;タグの前に空行を出力してHTMLブロックが途中で終了しないようにするなどの処理を行っています。ただし、&lt;figcaption&gt;タグに対応していないため画像のキャプションが見やすく表示されないなどの制限があります。</p>
<hr>
<p><a href="https&#58;//github.com/middle-river">[Home]</a></p>
<div align="right">
2021-04 Project finished.<br>2021-11-20 Page created.<br>2025-01-31 Support for GitHub README.md added.<br>T. Nakagawa
</div>
</body>
</html>
