#!/usr/bin/python

import random
from common import try_change_font_of_string

def test_cards(c):

    c.execute("select * from cards_local_view where datetime(nexptime,'utc') <= datetime('now')")

    rows = c.fetchall()
    random.shuffle(rows)
    test_rows(c,rows)


def search_cards(c):

    query = raw_input("query: ")

    c.execute("select * from cards_local_view where question like '%' || ? || '%'",
              (query,))

    rows = c.fetchall()
    random.shuffle(rows)
    test_rows(c,rows)


def test_rows(c,rows):

    def y_update(row):
        crct = row["crct"]+1
        c.execute("update cards set crct = ?,\
                   nexptime = datetime('now', ? || ' seconds')\
                   where rowid = ?",
                  (crct, random.randrange(2*60*60 << crct), row["rowid"]))
        return True

    def n_update(row):
        c.execute("update cards set crct = 0,\
        nexptime = datetime('now') where rowid = ?",
                  (row["rowid"],))
        return True

    def skip(row):
        return True

    def info_card(row):
        print row
        return False

    def delete_card(row):
        c.execute("delete from cards where rowid = ?",
                  (row["rowid"],))
        return True


    answer_query = {
        "y" : y_update,
        "n" : n_update,
        "s" : skip,
        "i" : info_card,
        "x" : delete_card
    }



    for row in rows:

        print try_change_font_of_string("31", "Q: " + row["question"])
        print "(press RET to see answer. Other keys ignored, except for 'quit' and 'skip')"

        q = raw_input()
        if q == "quit":
            break
        if q == "skip":
            continue
        if q == row["answer"]:
            print try_change_font_of_string("32", "CORRECT!")
            y_update(row)
            continue

        print try_change_font_of_string("34", "A: " + row["answer"])
        print "Got right answer? (%s)" % reduce(lambda s, other: s+"/"+other, answer_query.keys())
        while True:
            q = raw_input()
            if q in answer_query and answer_query[q](row):
                break



if __name__ == "__main__":

    import sys
    import sqlite3

    if len(sys.argv) != 2:
        print "usage: %s <tango file>" % sys.argv[0]
        exit()

    conn = sqlite3.connect(sys.argv[1])
    conn.text_factory = str
    conn.row_factory = sqlite3.Row
    c = conn.cursor()


    test_cards(c)

    conn.commit()
    conn.close()
