import re

import lxml
from lxml.html.clean import autolink_html


_link_regexes = [re.compile(
        r'(?P<body>https?://(?P<host>[a-z0-9._-]+)(?:/[/\-_.,a-z0-9%&?;=~:@#]*)?(?:\([/\-_.,a-z0-9%&?;=~:@#]*\))?)',
        re.I)]


def cleanup_chat_text(html):
    html = autolink_html(html, link_regexes=_link_regexes)

    html = lxml.html.fromstring(html)
    for a in html.cssselect('a'):
        a.attrib['target'] = '_blank'

    return lxml.html.tostring(html).decode('utf-8')


