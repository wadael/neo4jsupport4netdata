


# Neo4j support for NetData

----
# Status : Works on one machine, only 
I am sharing for getting help.
Developped on pc1 (OK), installed on pc2 (KO)

|Feature|pc1|pc2|
|---|---|---|
|os|mint |mint|
|netdata version |1.8|1.10|
| |  | |
----

-----


## Disclaimer
I am not a part of NetData or Neo4j, and not even a Python expert

## What is NetData ?

In one word: MONITORING !

As per the NetData website ( https://my-netdata.io/ )
Unparalleled insights, in real-time, of everything happening on your systems and applications, with stunning, interactive web dashboards and powerful performance and health alarms

The source code is on github at https://github.com/firehol/netdata/


## What is Neo4j ?

Neo4j is a graph database.
Everything you need to know is in [Learning Neo4j 2nd Edition](https://www.packtpub.com/big-data-and-business-intelligence/learning-neo4j-3x-second-edition?referrer=wadael)

# What does this support brings ?
It brings you three charts in their own menu.

* Total number of nodes
* Total number of nodes per label (top 5)
* Total number of nodes per relations (top 5) 



# Installation

## Install NetData
First, install NetData. 

I assume its done, else see the NetData's install page 

## Get this project's file
Download the files of this project and put them in the given destination folder. 

## Copy those files
Copy them in the given destination (as root).

Each .py file goes with a .conf file. The first is the code to create the graph, the latter is for the configuration.
You can install each pair or not.


|File name| Destination folder | Description|
|---|---|---|
| dashboard_info_custom.js | /usr/share/netdata/web | the js file describing the additionnal Neo4j menu |
| neo4jMon.chart.py | /usr/libexec/netdata/python.d |Total number of nodes | 
| neo4jMonLabels.chart.py |/usr/libexec/netdata/python.d |Total number of nodes per label (top 5 labels)| 
| neo4jMonRels.chart.py | /usr/libexec/netdata/python.d |Total number of nodes per relation (top 5 relations)| 
| neo4jMon.conf | /etc/netdata/python.d || 
| neo4jMonLabels.conf | /etc/netdata/python.d | | 
|neo4jMonRels.conf | /etc/netdata/python.d | | 
---

## Adapt

Open the /etc/netdata/netdata.conf file and add this line in the [web] paragraph (indent as needed)

```
[web]
    custom dashboard_info.js = dashboard_info_custom.js
```


The .conf files contain the credentials to connect to neo4j, and the server adress. 

If you rightfully not use neo4j/password, some change is needed. In each file.

## Get Neo4j Python driver
I tried to use pip and even pip3 without success so I just downloaded the driver from [Neo4j's website](https://pypi.org/project/neo4j-driver/1.5.3/#files) and (as root), and extracted the 
  - neo4j
  - neo4j_driver.egg-info 
folders in /usr/libexec/netdata/python.d/python_modules


## Give back ownership + group
All files added/modified must belong to netdata/netdata.

cd /usr/libexec/netdata/
sudo chown -R netdata * && chgrp -R netdata *

Same for /etc/netdata/ and /usr/share/netdata/web


## Start Neo4j
Well, easy to miss this step 

## Restart NetData
As root, for ubuntu and variants 
```
service netdata restart
``` 

## Enjoy
Go to http://localhost:19999 and enjoy.
Give it an instant to show the Neo4j related graphs err ... charts

Refresh screen if needed 



# Troubleshooting
* verify ports in the conf files
* check the file /var/log/netdata/error.log
* replace tabs by spaces in the .py files (if you modified them)
* I had the issue of NetData not finding the neo4j-driver, you have to install it or run the modified shell script. Is there a /usr/libexec/netdata/python.d/python_modules folder ?



#  Oh files, where art thou ?

   - the daemon     at  /usr/sbin/netdata
   - config files   in  /etc/netdata
   - web files      in  /usr/share/netdata
   - plugins        in  /usr/libexec/netdata
   - cache files    in  /var/cache/netdata
   - db files       in  /var/lib/netdata
   - log files      in  /var/log/netdata
   - pid file       at  /var/run/netdata.pid
   - logrotate file at  /etc/logrotate.d/netdata



# FAQ


## Shouldn't this be part of NetData ?
Probably, I have not yet contacted the authors of NetData or proposed a PR. Yet, I want a few buddies to try this. So I published it.


## How do you like NetData ?

Very much. Its a very useful tool


## What are the pros ?

Use this project to conveniently check that your imports are going well. Of course you could repeatedly query yourself but hey, why not fancy charts, mate ? 

# What are the cons ?
If the top 5 labels are replaced by others, the legend will have 10 label names. Easily solve this by clearing the cache.


# Acknowledgements
As an almost total Python noob, this project would not work without the examples provided by the NetData and Neo4j Python driver teams.

