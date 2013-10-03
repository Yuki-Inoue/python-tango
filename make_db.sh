#!/bin/bash

for db in $*
do
    sqlite3 $db "
CREATE TABLE cards
(nexptime datetime, crct int, question text, answer text);
CREATE VIEW cards_local_view as
select rowid,datetime(nexptime,'localtime') as nexptime,crct,question,answer
from cards;
"
done
