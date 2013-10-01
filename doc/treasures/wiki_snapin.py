#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2013             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

#!/usr/bin/python
#Author Bastian Kuhn <bk@mathias-kettner.de>

#This file is a Multisite Snapin which will show
#a the dokuwiki navigation menu if set
#Place the file to ~/local/share/check/web/plugins/sidebar
#and restart apacher.

def render_wiki():
    import re
    filename = defaults.omd_root + '/var/dokuwiki/data/pages/sidebar.txt'
    start_ul = True
    ul_started = False
    try:
        title = None
        for line in file(filename).readlines():
            line = line.strip()
            if line == "":
                if ul_started == True:
                    html.end_foldable_container()
                    start_ul = True
                    ul_started = False
            elif line.endswith(":"):
                title = line[:-1]
            elif line == "----":
                pass
                # html.write("<br>")

            elif line.startswith("*"):
                if start_ul == True:
                    if title:
                         html.begin_foldable_container("wikisnapin", title, True, title, indent=True)
                    start_ul = False
                    ul_started = True

                erg = re.findall('\[\[(.*)\]\]', line)
                if len(erg) == 0:
                    continue
                erg = erg[0].split('|')
                if len(erg) > 1:
                    link = erg[0]
                    name = erg[1]
                else:
                    link = erg[0]
                    name = erg[0]


                if link.startswith("http://") or link.startswith("https://"):
                    simplelink(name, link, "_blank")
                else:
                    erg = name.split(':')
                    if len(erg) > 0:
                        name = erg[-1]
                    else:
                        name = erg[0]
                    bulletlink(name, "/%s/wiki/doku.php?id=%s" % (defaults.omd_site, link))

            else:
                html.write(line)

        if ul_started == True:
            html.write("</ul>")
    except IOError:
        html.write("You have to create a sidebar first")
        
    html.write("<hr>")
    html.javascript("""
    function wiki_search()
    {
        var oInput = document.getElementById('wikisearch_input');
        top.frames["main"].location.href = 
           "/%s/wiki/doku.php?do=search&id=" + escape(oInput.value);
    }
    """ % defaults.omd_site)
    html.begin_form("wikisearch", onsubmit="wiki_search();")
    html.text_input("wikisearch", "", id="wikisearch_input", )
    html.icon_button("#", _("Search"), "wikisearch", onclick="wiki_search();")
    html.end_form()

if defaults.omd_root:
    sidebar_snapins["wiki"] = {
        "title" : _("Wiki"),
        "description" : _("Shows the Wiki Navigation of the OMD Site"),
        "render" : render_wiki,
        "allowed" : [ "admin", "user", "guest" ],
        "styles" : """
        #snapin_container_wiki div.content {
            font-weight: bold;
            color: white;
        }
        input#wikisearch_input {
    #        margin-top: 3px;
    #        width: 222px;
    margin:  0;
    padding: 0px 5px;
    font-size: 8pt;
    width: 194px;
    height: 25px;
    background-image: url("images/quicksearch_field_bg.png");
    background-repeat: no-repeat;
    -moz-border-radius: 0px;
    border-style: none;
    float: left;
        }
        #snapin_container_wiki hr {
            margin: 5px 2px;
        }
        #snapin_container_wiki ul {
            margin: 1px;
        }
#wikisearch img.iconbutton {
    width: 33px;
    height: 26px;
    margin-top: -25px;
    left: 196px;
    float:right;
    z-index:100;
}
    
        """
    }
    
