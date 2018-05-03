#/bin/bash

LEDIR=$(pwd)

cd /usr/libexec/netdata/
sudo chown -R netdata * && chgrp -R netdata *

cd /etc/netdata/
sudo chown -R netdata * && chgrp -R netdata *

cd /usr/share/netdata/web
sudo chown -R netdata * && chgrp -R netdata *

cd LEDIR

