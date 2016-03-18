# This script grabs tickets from project locker and creates an html and css file to display
# all current, active tickets. 

from xmlrpclib import ServerProxy
import datetime
import sys


if len(sys.argv) != 4:
  sys.exit("Not enough args")
username = str(sys.argv[1])
pw = str(sys.argv[2])
projectName = str(sys.argv[3])

# Connect to the project locker, grab all the ticket numbers and each ticket associated with
# it
p = ServerProxy('https://%s:%s@pl2.projectlocker.com/MazamaScience/%s/trac/login/rpc' % (username, pw, projectName))
ticketNums  = p.ticket.query()
tickets = [p.ticket.get(num) for num in ticketNums]
# Each ticket is a list of 4 things, the first is the number, 2nd and 3rd are datetimes and
# the 4th is a dicitonary with all the information for the ticket (like description) but it
# doesn't have the ticket number or date so were going to put that in.
for i in range(len(ticketNums)):
    tickets[i][3]['ticketNum'] = ticketNums[i]
    date = tickets[i][2]
    date = datetime.datetime.strptime(date.value, "%Y%m%dT%H:%M:%S")
    tickets[i][3]['date'] = datetime.datetime.strftime(date, "%B %d, %Y at %H:%M:%S")

# Lets make a dictionary of tickets with ticket numbers for keys
tickets = dict(zip(ticketNums, [ticket[3] for ticket in tickets]))

# For each ticket were going to use replace an html skeleton of a ticket with all the tickets
# information and put it in a list.
html = []
for key in tickets:
    ticket = tickets[key]
    format = '''
    <div id="ticket">
          <!-- use a placeholder if it's a new ticket -->
          <h2 class="summary searchable"><b>Ticket #%s</b> %s</h2>
          <table class="properties">
            <tr>
              <th id="h_reporter">Reported by:</th>
              <td headers="h_reporter" class="searchable">%s</td>
              <th id="h_owner">Owned by:</th>
              <td headers="h_owner">%s
              </td>
            </tr>
            <tr>
                <th id="h_priority">
                  Priority:
                </th>
                <td headers="h_priority">
                      %s
                </td>
                <th id="h_milestone">
                  Milestone:
                </th>
                <td headers="h_milestone">
                      %s
                </td>
            </tr><tr>
                <th id="h_component">
                  Component:
                </th>
                <td headers="h_component">
                      %s
                </td>
                <th id="h_version">
                  Version:
                </th>
                <td headers="h_version">
                  %s
                </td>
            </tr><tr>
                <th id="h_keywords">
                  Keywords:
                </th>
                <td headers="h_keywords" class="searchable">
                  %s
                </td>
                <th id="h_cc">
                  Cc:
                </th>
                <td headers="h_cc" class="searchable">
                  %s
                </td>
            </tr>
          </table>
            <div class="description">
              <h3 id="comment:description">
                Description
              </h3>
              <div class="searchable">
                <p>
%s
</p>

              </div>
            </div>
        </div>
''' % ( ticket['ticketNum'], ticket['summary'], ticket['reporter'], ticket['owner'], ticket['priority'], ticket['milestone'], ticket['component'], ticket['version'], ticket['keywords'], ticket['cc'], ticket['description'])
    html.append(format)

# Lets make this actual runable html code, also put in a refrence to the css file.
html.append('</body>\n</html>')
html.insert(0, '<html>\n<head>\n <link rel="stylesheet" href="ticket.css" type="text/css"> \n</head>\n<body>')

with open('tickets.html', 'w') as f:
    f.write('\n'.join(html))

# The code below copies and writes a css file for tickets. I grabbed this from project locker
# and not all of it is needed.
css = '''
@import url(code.css);

#content.ticket { width: 700px; max-width: 100% }

#newticket #field-description { width: 100% }
#newticket #properties { width: 100% }

#ticket {
 background: #ffd;
 border: 1px outset #996;
 margin-top: 1em;
 padding: .5em 1em;
 position: relative;
}

div#ticket.ticketdraft {
 background: #f4f4f4 url(../draft.png);
}
div#ticketchange.ticketdraft {
 padding: 0 1em;
 margin: 1em 0;
}
div#ticketchange.ticketdraft h3 {
 margin-top: .5em;
}
.preview-notice { font-weight: bold; }

.ticketdraft {
 background: #f4f4f4 url(../draft.png);
 border: 1px outset #996;
 padding: 0 .2em;
}

h1 .status { color: #444; }
#ticket h2.summary { margin: 0 0 .8em 0 }
#ticket .date { color: #996; float: right; font-size: 85%; position: relative }
#ticket .date p { margin: .3em }

#ticket table.properties {
 clear: both;
 border-top: 1px solid #dd9;
 border-collapse: collapse;
 table-layout: fixed;
 width: 100%;
}
#ticket table.properties tr { border-bottom: 1px dotted #eed }
#ticket table.properties td, #ticket table.properties th {
 font-size: 80%;
 padding: .5em 1em;
 vertical-align: top;
}
#ticket table.properties th {
 color: #663;
 font-weight: normal;
 text-align: left;
 width: 20%;
}
#ticket table.properties td { width: 30% }
#ticket table.properties td p:first-child { margin-top: 0 }
#ticket table.properties td p:last-child { margin-bottom: 0 }
#ticket table.properties .description { border-top: 1px solid #dd9 }

#ticket .description h3 {
 border-bottom: 1px solid #dd9;
 color: #663;
 font-size: 100%;
 font-weight: normal;
}
#ticket .description h3 .lastmod {
 font-size: 90%;
}
#ticket .inlinebuttons { 
 float: right;
 position: relative;
 bottom: 0.3em;
}

#changelog { border: 1px outset #996; padding: 1em }
#preview { border: 1px solid #d7d7d7; padding: 1em }
#preview h3, #changelog h3 {
 border-bottom: 1px solid #d7d7d7;
 color: #999;
 font-size: 100%;
 font-weight: normal;
}
.threading, #changelog .inlinebuttons { float: right; }
.threading { font-size: 90%; }

#preview .changes, #changelog .changes { list-style: square; margin-left: 2em; padding: 0 }
#preview .comment, #changelog .comment { margin-left: 2em }

form .field { margin-top: .75em; width: 100% }
form #comment { width: 100% }

#properties { white-space: nowrap; line-height: 160%; padding: .5em }
#properties table { border-spacing: 0; width: 100%; }
#properties table th {
 padding: .4em;
 text-align: right;
 width: 20%;
 vertical-align: top;
}
#properties table th.col2 { border-left: 1px dotted #d7d7d7 }
#properties table td { vertical-align: middle; width: 30% }
#properties table td.fullrow { vertical-align: middle; width: 80% }

#action { line-height: 2em }

fieldset.radio { border: none; margin: 0; padding: 0 }
fieldset.radio legend {
 color: #000;
 float: left;
 font-size: 100%;
 font-weight: normal;
 padding: 0 1em 0 0;
}
fieldset.radio label { padding-right: 1em }


'''

with open('ticket.css', 'w') as f:
    f.write(css)
    
print "done!"
