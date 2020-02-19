#!/bin/bash
echo "1. "
find /usr/share/man -name "stat*"

echo "2. "
find /usr/share/man -name "stat*" | sort | uniq -c

echo "3. "
find /usr/share/man -name "stat*" | cut -b 16-19 | sort | uniq -c

echo "4. "
find /usr/share/man -name "stat*" | xargs file -b

echo "5. "
find /usr/share/man -name "stat*" | xargs -I {} bash -c "zcat {} | groff -man -Thtml > file.html"

echo "6. "
find /usr/share/man -name "stat*" | xargs -P 2 bash -c 'zcat | groff -mandoc -Thtml'

echo "7. "
find /usr/share/man -name "stat*" | parallel 'zcat {} | groff -mandoc -Thtml > /srv/www/man/`basename {} .gz`.html'
