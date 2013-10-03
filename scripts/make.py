#!/usr/bin/python

def make_card(c,question=None,answer=None):

    question_query = "Question: "
    answer_query   = "Answer  : "

    fail_message = "failed in making!"

    if not question:
        question = raw_input(question_query)
    if not question:
        print fail_message
        return

    if not answer:
        answer = raw_input(answer_query)
    if not answer:
        print fail_message
        return

    c.execute("""insert into cards(nexptime, crct, question, answer)
    values(datetime('now'), 0, ?, ?)""", (question, answer))

    c.execute("select * from cards_local_view where rowid = last_insert_rowid()")

    return c.fetchone()


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

    make_card(c)

    conn.commit()
    conn.close()
