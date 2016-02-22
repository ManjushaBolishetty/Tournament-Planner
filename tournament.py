#importing the db adapter for python
import psycopg2
import pprint

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    # print("Deleting matches")
    cur.execute("delete from Matches")
    db.commit()
    # print("Deleted matches")
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE from Players")
    db.commit()
    db.close()

def deleteScoreboard():
    '''clean all the data in the table scoreboard'''
    db = connect()
    cur = db.cursor()
    cur.execute("delete from Scoreboard")
    db.commit()
    db.close()

def deleteTournament():
    """Remove all the records from the tournament table."""
    db = connect()
    cur = db.cursor()
    cur.execute("DELETE from Tournament")
    db.commit()
    db.close()

def createTournament(Tdesc):
    """create an entry in the tournament table for each tournament.
    Args:
        Tdesc: Description of the tournament like Test, Finals for example.
    Returns:
        int: Tid (tournament_id)."""
    db = connect()
    cur = db.cursor()
    insert_tournament = "insert into Tournament(tournament_desc) values (%s) RETURNING tournament_id"
    cur.execute(insert_tournament,(Tdesc,))
    Tid = cur.fetchone()[0]
    db.commit()
    db.close()
    return Tid

def countPlayers(Tid):
    """count the players registered for a given tournament
    Args:
        Tid: Input is the tournament_id referred to as Tid here.
    Returns:
        int: count_players - count of players for a gien tournament."""
    db = connect()
    cur = db.cursor()
    select_sql = """select count(player_id) as num_players from Scoreboard
    where tournament_id = %s"""
    cur.execute(select_sql,(Tid,))
    count_players = cur.fetchone()[0]
    db.close()
    # print ("In counterPlayers:%s" %count_players)
    return count_players

def registerPlayer(name,Tid):
    """register the players
    Args:
        Tid: Input is the tournament_id referred to as Tid here.
        name: name of the player """
    db = connect()
    cur = db.cursor()
    player_name = "INSERT INTO players (player_name) VALUES (%s) RETURNING player_id"
    scoreboard = "INSERT INTO Scoreboard (tournament_id,player_id,score,num_matches,num_bye) VALUES (%s,%s,%s,%s,%s)"
    cur.execute(player_name, (name,))
    player_id = cur.fetchone()[0]
    cur.execute(scoreboard, (Tid,player_id,0,0,0))
    db.commit()
    db.close

def playerStandings(Tid):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cur = db.cursor()
    players="""select sb.player_id, p.player_name,sb.score, sb.num_matches,sb.num_bye ,
    (select sum(sb1.score) from Scoreboard sb1 where
    sb1.player_id in (Select losser_id from matches where winner_id =  sb.player_id and tournament_id = %s)
    OR sb1.player_id in (Select winner_id from matches where losser_id =  sb.player_id and tournament_id = %s))
    as scores_ps from Scoreboard sb, players p where
    p.player_id = sb.player_id and sb.tournament_id = %s
    order by sb.score desc, scores_ps desc, sb.num_matches desc """
    cur.execute(players,(Tid,Tid,Tid))
    player_rank = []
    for i in cur.fetchall():
        player_rank.append(i)
    db.close()
    # pprint.pprint("In playerStandings:%s" % player_rank)
    return player_rank

def reportMatch(Tid,winner_id,losser_id,draw='FALSE'):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    if(draw == 'TRUE'):
        winner_score = 1
        losser_score = 1
    else:
        winner_score = 3
        losser_score = 0
    db = connect()
    cur = db.cursor()
    insert_matches = "INSERT INTO matches (tournament_id, winner_id, losser_id, draw) VALUES (%s,%s,%s,%s)"
    winner_upd = "UPDATE scoreboard SET score = score+%s, num_matches = num_matches+1 WHERE player_id = %s AND tournament_id = %s"
    losser_upd = "UPDATE scoreboard SET score = score+%s, num_matches = num_matches+1 WHERE player_id = %s AND tournament_id = %s"
    cur.execute(insert_matches,(Tid, winner_id, losser_id, draw))
    cur.execute(winner_upd,(winner_score, winner_id, Tid))
    cur.execute(losser_upd,(losser_score, losser_id, Tid))
    db.commit()
    db.close()

def hasBye(player_id, Tid):
    db = connect()
    cur = db.cursor()
    selection = """SELECT num_bye
             FROM scoreboard
             WHERE player_id = %s
             AND tournament_id = %s """
    cur.execute(selection, (player_id,Tid))
    num_bye = cur.fetchone()[0]
    db.close()
    # print("In hasBye:num_bye:%s" %num_bye)
    if num_bye == 0:
        return False
    else:
        return True


def reportBye(player_id, Tid):
    """Update table scoreboard with the details for a player who should have a bye(free - win)
    Args:
        player_id: Id of the player from the players table
        Tid : tournament id associated with the pair of players"""
    db = connect()
    cur = db.cursor()
    bye_upd = "UPDATE scoreboard SET score = score+3, num_bye=num_bye+1 WHERE player_id = %s AND tournament_id = %s"
    cur.execute(bye_upd, (player_id,Tid))
    db.commit()
    db.close()

def checkByes(Tid, rankings, index):
## Recheck this logic when 2 players are there none should have a bye. Check condition when a bye is assigned
    """Returns an index value. Checks if a player has a bye already
    Args:
        Tid : tournament id associated with the pair of players
        ranking: playerstanding
        index: position of the player from the players table whose records are being checked for byes
    Returns:
        int: -1 or 0 if the player has no bye
    """
    len_rankings = len(rankings)
    # print("In checkByes: %s"  % len_rankings)
    if abs(index) > len(rankings):
        # print("in if)")
        return -1
    elif not hasBye(rankings[index][0], Tid):
        # print("In Elif not")
        return 0
    else:
        return checkByes(Tid, rankings, (index - 1))

def validPair(player1, player2, Tid):
    """Returns player_id after checking for validpairs
    Args:
        player1: id of the first player
        player2: id of the second player
        Tid : tournament id associated with the pair of players
    Returns:
        bool: True if it is a valid pair else false
    """
    db = connect()
    cur = db.cursor()
    checkValidPair= """SELECT winner_id, losser_id
                        FROM matches
                        WHERE ((winner_id = %s AND losser_id = %s)
                        OR (winner_id = %s AND losser_id = %s))
                        AND tournament_id = %s"""
    cur.execute(checkValidPair, (player1, player2, player2, player1, Tid))
    count_matches = cur.rowcount
    db.close()
    if count_matches > 0:
        return False
    return True

def checkPairs(Tid, rankings, player_id1, player_id2):
    """Returns player_id after checking for validpairs
    Args:
        Tid : tournament id associated with the pair of players
        rankings: standing for the match
        player_id1: id of the first player
        player_id2: id of the second player
    """
    if player_id2 >= len(rankings):
        return player_id1 + 1
    elif validPair(rankings[player_id1][0], rankings[player_id2][0], Tid):
        return player_id2
    else:
        return checkPairs(Tid, rankings, player_id1, (player_id2 + 1))

def swissPairings(Tid):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    rankings = playerStandings(Tid)
    pairs = []

    num_Players = countPlayers(Tid)
    if num_Players % 2 != 0:
        bye = rankings.pop(checkByes(Tid, rankings, -1))
        reportBye(bye[0],Tid)
        # print("In Swisspairing")
        # print(bye[0])
        # print(Tid)

    while len(rankings) > 1:
        valid_match = checkPairs(Tid,rankings,0,1)
        player1 = rankings.pop(0)
        player2 = rankings.pop(valid_match - 1)
        pairs.append((player1[0],player1[1],player2[0],player2[1]))
    return pairs
