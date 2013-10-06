#!/usr/bin/python

if __name__ == "__main__":

    import sys

    if len(sys.argv) == 1:
        print "usage: %s <tango files>" % sys.argv[0]
        exit()

    import sqlite3
    import random
    from scripts import make_card, test_cards, search_cards, try_change_font_of_string

    random.seed()

    for tango_file in sys.argv[1:]:

        print try_change_font_of_string("1", "In %s" % tango_file)

        conn = sqlite3.connect(tango_file)
        conn.text_factory = str
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        def calc_expired():
            c.execute("select count(*) from cards where nexptime <= datetime('now')")
            return c.fetchone()[0]

        expired = calc_expired()

        if len(sys.argv) > 2 and not expired:
            print "skipping this file!"
            continue


        qa_flag = False

        while True:
            print "%s expired" % expired
            q = raw_input("> ")
            if q == "q":
                break
            elif q == "w":
                conn.commit()
            elif q == "wq":
                conn.commit()
                break
            elif q == "qa":
                qa_flag = True
                break
            elif q == "wqa":
                qa_flag = True
                conn.commit()
                break
            elif q == "m":
                print make_card(c)
            elif q == "t":
                test_cards(c)
            elif q == "s":
                search_cards(c)
            else:
                print "(q/wq/qa/wqa/m/t/s)"
            expired = calc_expired()

        conn.close()

        if qa_flag:
            break
