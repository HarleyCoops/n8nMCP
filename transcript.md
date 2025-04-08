0:00
hey everyone welcome back today I'm
0:02
going to show you how to install NN
0:05
using Docker completely free and then
0:07
take it to the next level by
0:09
supercharging AI agents with mCP model
0:12
context protocol imagine this your AI
0:15
instantly connects to any tool or API no
0:18
messy HTTP requests no endless API docks
0:22
just pure automation magic that's
0:24
exactly what mCP does it standardizes
0:27
tool execution making automation faster
0:30
smarter and 10x easier here's what
0:32
you'll master in just a few minutes
0:35
install n8n locally using Docker so you
0:38
can use it completely free set up mCP in
0:41
n8n to unlock powerful AI automation
0:45
enable AI Define and execute the best
0:47
tool dynamically no hard coding needed
0:50
automate web searches and web scraping
0:52
effortlessly using mCP and here's the
0:55
kicker stick around till the end because
0:57
I'll be revealing a secret automation
0:59
trick that even experienced AI Engineers
1:02
don't know yet smash that like button
1:04
subscribe and turn on the Bell icon so
1:07
you never miss an automation hack before
1:09
we set up NN let's quickly understand
1:12
what Docker is and why it's a
1:14
GameChanger for automation think of
1:16
Docker as a virtual container system for
1:19
apps instead of installing software
1:21
directly on your computer Docker lets
1:23
you run applications in isolated
1:25
self-contained environments called
1:27
containers this means no messy and
1:29
installations no dependency conflicts
1:32
and no worrying about breaking your
1:34
system with Docker we can run NN in a
1:37
lightweight portable and secure
1:39
environment making it super easy to set
1:41
up and manage now that we know why
1:43
Docker is amazing let's install Docker
1:46
desktop go to the official Docker
1:48
website download the version for your
1:50
operating system Windows or Mac run the
1:53
installer and follow the simple onscreen
1:55
instructions once installed open Docker
1:57
desktop and make sure it's running
1:59
before moving forward now that we have
2:01
Docker desktop running let's pull down
2:04
the N image and set up our AI automation
2:07
environment in Docker desktop go to the
2:10
search box at the top Type n and select
2:13
the official Nan image from the list
2:16
click download to pull the latest na
2:19
image wait for the download to complete
2:21
it may take a few moments depending on
2:23
your internet speed now that we have the
2:25
image let's create a new container next
2:29
go to the images tab in Docker desktop
2:32
find the N image and click the Run
2:35
button now let's configure it before we
2:38
start give your container a meaningful
2:40
name let's call it NN container we need
2:43
to specify a port so we can access n via
2:47
a browser set it to
2:49
5678 or any other number you prefer so
2:52
we can access NN on that port to ensure
2:56
that our workflows and user settings are
2:58
saved we need to configure a volume in
3:01
the volume section set the host path to
3:04
a local folder where you want to store
3:06
n's data for the container path set it
3:10
to this
3:12
path since we want to use AI agents with
3:16
mCP in NN we need to update the
3:19
environment variables we will need to
3:21
add this variable set the value to true
3:24
to enable Community nodes as tools
3:26
inside n
3:30
once everything is set up click the Run
3:32
button to start the container give it a
3:35
few seconds to initialize now let's
3:38
check if it's working open your browser
3:40
and go to Local Host on the port we just
3:42
set up you should now see the NN signup
3:46
screen let's create an account fill in
3:49
all the necessary details including your
3:51
username email and password follow the
3:54
instructions to set up a new account
4:01
now click on this button to start a new
4:04
workflow awesome n8n is now fully set up
4:08
and ready to use next let's install mCP
4:12
servers inside NN this will allow our AI
4:15
agents to interact seamlessly with
4:17
external tools and data sources navigate
4:20
to the setting section go to the
4:22
community nodes
4:25
tab here let's search for n8n nodes and
4:29
mCP then click install and wait for the
4:33
installation to complete once installed
4:35
you'll have access to mCP
4:37
functionalities within your
4:39
workflows return to the workflow section
4:42
and name your
4:43
workflow let's say mCP server
4:47
agent okay next to initiate our workflow
4:51
based on user chat input We'll add a
4:53
chat trigger
4:54
node all right now we're going to add an
4:56
AI agent node to the workflow after
4:59
receiving the user's chat message this
5:02
node enables the agent to utilize
5:04
external tools and apis to perform
5:07
actions and retrieve information now
5:09
let's configure the AI agent node to use
5:12
the open AI chat model to use the model
5:14
you should create a new credential here
5:17
Ure you have an open AI account and have
5:19
generated an API key from the open AI
5:22
website here then input your open AI API
5:25
key into the noes credentials and hit
5:28
save button
5:32
we leave the desired model as GPT 40
5:36
mini to allow our agent to retain
5:38
conversational context we'll incorporate
5:41
a simple memory node so let's add the
5:44
simple memory node to the workflow and
5:46
connect it appropriately now let's
5:49
Empower our AI agent by integrating
5:51
model context protocol servers providing
5:54
it with robust tools for complex tasks
5:57
first of all We'll add the mCP client to
6:00
see how it works there's a list of
6:02
actions here let's try using this action
6:05
to list the available tools next we need
6:07
to add credentials to connect to the mCP
6:10
server here we're using the command line
6:13
to integrate an mCP server with MPX in
6:16
the command field the arguments will
6:18
include the mCP server name to explore
6:21
available mCP servers we'll visit their
6:24
GitHub page where we can see all the
6:26
server tools available for our workflow
6:28
for this example example we'll use the
6:30
brave search server which allows us to
6:32
search for businesses restaurants and
6:35
services with detailed information to
6:37
use this mCP Brave server we need an API
6:40
key from the brave search API so let's
6:43
create a new account to obtain the key
6:46
and copy it for later
6:48
use next we'll add the mCP server name
6:52
to the argument field and input the
6:54
brave API key
7:02
all right finally we need to update the
7:05
environment with the brave API
7:10
key fill in the brave API key we just
7:15
copied after hitting save we specify the
7:18
action list tools for the operation now
7:22
we can test this node to retrieve the
7:24
available Brave tools we have two Brave
7:26
tools here along with their capabilities
7:30
awesome now that we know how to use the
7:32
mCP node in NN let's add an mCP server
7:37
as a tool for the AI agent we'll remove
7:39
the current mCP example click the plus
7:42
icon to add a new node for the agent and
7:45
select the mCP client to fetch a list of
7:48
Brave tools make sure to choose the
7:50
credentials we just created finally we
7:53
add another mCP node to allow the agent
7:56
to execute the tools
8:00
configure the AI agent to utilize the
8:02
tools retrieved from the brave search
8:04
mCP server set the operation to execute
8:07
tool and specify the tool name obtained
8:10
from the previous mCP nodes tools
8:13
configure the tool parameters as needed
8:16
or allow the model to Define them
8:21
automatically before running the
8:23
workflow let's define a system message
8:25
to guide the AI agent in its role such
8:28
as you are a helpful assistant utilizing
8:30
Brave search to perform web queries
8:33
alternatively you can use our system
8:36
message next ensure all nodes are
8:39
properly connected to facilitate smooth
8:41
data flow and execution within the
8:43
workflow once everything is set we're
8:45
ready to test the workflow open the chat
8:48
box and send a message asking the agent
8:50
about restaurants or
8:52
cafes monitor the workflow execution to
8:55
make sure the AI agent interacts with
8:57
the mCP server as expected let's dive
9:00
into how our AI agent processes user
9:02
inputs initially the agent captures both
9:05
the user's message and the predefined
9:07
system instructions storing them in the
9:10
simple memory node this ensures context
9:13
is maintained throughout the interaction
9:15
the stored messages are then forwarded
9:17
to the open AI chat model node here the
9:20
AI interprets the user's request and
9:22
determines that utilizing the brave
9:24
Search tool is the optimal approach to
9:26
fulfill the task the AI agent the mCP
9:30
client node to interface with the brave
9:32
search mCP server it performs the
9:35
necessary search operations based on the
9:37
user's query after obtaining the search
9:40
results the Open aai chat model
9:42
processes the data transforming it into
9:45
a coherent and informative response
9:47
tailored for the user finally the AI
9:50
agent delivers the human readable
9:51
information back to the user effectively
9:54
completing the workflow Awesome by
9:58
integrating mCP servers like Brave
10:00
search into our n8n workflows we've
10:03
empowered our AI agents to perform
10:06
complex tasks efficiently providing
10:08
users with accurate and timely
10:10
information stay tuned for more
10:12
tutorials on enhancing your automation
10:14
workflows if you found this guide
10:16
helpful like subscribe and hit the
10:19
notification Bell to stay updated with
10:21
the latest automation tips see you in
10:23
the next
10:26
[Music]
10:28
video what