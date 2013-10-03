#!/bin/bash

for db in $*
do
    sqlite3 $db "create view cards_local_view as select rowid,datetime(nexptime,'localtime') as nexptime,crct,question,answer from cards"
done
