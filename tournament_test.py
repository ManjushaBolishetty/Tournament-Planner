from tournament import *

def testDeleteMatches():
    #Function tests the delete functionality for the table matches
    deleteMatches()
    print "1. Old matches can be deleted."

def testDelete():
    #Function tests the delete functionality for the tables matches, players, tournament, scoreboard
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    print "2. Player records can be deleted"

def testCount():
    #Function tests the creation of a record in tournament table and the count of players after the delete
    #operation on the tables matches, players, tournament, scoreboard
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    c = countPlayers(Tid)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."

def testRegister():
    #Function tests the creation of a record in tournament table and the count of players
    #afer registering for a match.
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Chandra Nalaar",Tid)
    c = countPlayers(Tid)
    if c != 1:
        raise ValueError("After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."

def testRegisterCountDelete():
    #Functionality to test countPlayers() after deletion
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Markov Chaney",Tid)
    registerPlayer("Joe Malik",Tid)
    registerPlayer("Mao Tsu-hsi",Tid)
    registerPlayer("Atlanta Hope",Tid)
    c = countPlayers(Tid)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deleteScoreboard()
    c = countPlayers(Tid)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Melpomene Murray", Tid)
    registerPlayer("Randy Schwartz", Tid)
    before_standings = playerStandings(Tid)
    if(len(before_standings) < 2):
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")

    elif len(before_standings) > 2:
        raise ValueError("Only registered players should appear in standings.")

    if len(before_standings[0]) != 6:
        raise ValueError("Each playerStandings row should have four columns.")

    [(player_id1, player_name1,scores1, num_matches1,num_bye1, scores_ps1), (player_id2, player_name2,scores2, num_matches2,num_bye2,scores_ps2)] = before_standings
    if(num_matches1 != 0 or num_matches2 != 0 or scores1 != 0 or scores2 != 0 or num_bye1 != 0 or num_bye2 != 0 ):
        raise ValueError("Newly registered players should have no matches or wins.")
    if set([player_name1, player_name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Bruno Walton", Tid)
    registerPlayer("Boots O'Neal", Tid)
    registerPlayer("Cathy Burton", Tid)
    registerPlayer("Diane Grant", Tid)
    beforeStandings = playerStandings(Tid)
    [player_id1, player_id2, player_id3, player_id4] = [i[0] for i in beforeStandings]
    reportMatch(Tid, player_id1, player_id2)
    reportMatch(Tid, player_id3, player_id4, 'TRUE')
    afterStandings = playerStandings(Tid)
    for (i, n, s, m, b, o) in afterStandings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i == player_id1 and s != 3:
            raise ValueError("Each winner gets 3 points and the victory should be recorded.")
        elif i in (player_id3, player_id4) and s != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i == player_id2 and s != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."

def testReportBye():
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Bruno Walton", Tid)
    # registerPlayer("Manjusha", Tid)
    standings = playerStandings(Tid)
    player_id = standings[0][0]
    reportBye(player_id, Tid)
    standings = playerStandings(Tid)
    for i in standings:
        if i[4] != 1:
            raise ValueError("The player must have a bye recorded")
    print "8. All Byes are reported"

def testHasBye():
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Bruno Walton", Tid)
    # registerPlayer("Manjusha", Tid)
    standings = playerStandings(Tid)
    player_id = standings[0][0]
    reportBye(player_id, Tid)
    if not hasBye(player_id, Tid):
        raise ValueError("The player should have a bye")
    print "9. Byes are validated"


def testCheckByes():
    #Checks the functionality if a player has already been assigned a bye.
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Bruno Walton", Tid)
    registerPlayer("Boots O'Neal", Tid)
    # print("In testCheckByes: bef_standings")
    bef_standings = playerStandings(Tid)
    player_id = bef_standings[-1][0]
    # print("player_id:%s" %player_id)
    num_Players = countPlayers(Tid)
    if(num_Players % 2 != 0):
        reportBye(player_id, Tid)
    # print("In testCheckByes: after_standings")
    after_standings = playerStandings(Tid)
    test = checkByes(Tid, after_standings, -1)
    # print(test)
    if test == -1:
        raise ValueError("The player already has a bye.")
    print "10. Byes are assigned properly."
#
def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Twilight Sparkle", Tid)
    registerPlayer("Fluttershy", Tid)
    registerPlayer("Applejack", Tid)
    registerPlayer("Pinkie Pie", Tid)
    standings = playerStandings(Tid)
    [player_id1, player_id2, player_id3, player_id4] = [i[0] for i in standings]
    reportMatch(Tid, player_id1, player_id2)
    reportMatch(Tid, player_id3, player_id4)
    pairings = swissPairings(Tid)
    if len(pairings) != 2:
        raise ValueError(
            "swissPairings() should return 2 pairs for 4 players playing the match.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([player_id1, player_id3]), frozenset([player_id2, player_id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError("After one match, players with one win should be paired.")
    print "11. After one match, players with one win should be paired."

def testOddPairings():
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("Twilight Sparkle", Tid)
    registerPlayer("Fluttershy", Tid)
    registerPlayer("Applejack", Tid)
    registerPlayer("Pinkie Pie", Tid)
    registerPlayer("Bye Bye", Tid)
    standings = playerStandings(Tid)
    num_Players = countPlayers(Tid)
    player_bye = standings[-1][0]
    if(num_Players % 2 != 0):
        reportBye(player_bye, Tid)
    [player_id1, player_id2, player_id3, player_id4, player_id5] = [i[0] for i in standings]
    reportMatch(Tid, player_id1, player_id2)
    reportMatch(Tid, player_id3, player_id4)
    pairings = swissPairings(Tid)
    if len(pairings) != 2:
        raise ValueError("swissPairings() should return 2 pairs for 5 registered players.")
    [(player_id1, player_name1, player_id2, player_name2), (player_id3, player_name3, player_id4, player_name4)] = pairings
    correct_pairs = set([frozenset([player_id1, player_id3]), frozenset([player_id2, player_id4])])
    actual_pairs = set([frozenset([player_id1, player_id2]), frozenset([player_id3, player_id4])])
    if correct_pairs != actual_pairs and not hasBye(player_id5, Tid):
        raise ValueError("The last player incase of odd number of registered player receives a free win(Bye)")
    print "12. With odd number, last player should have bye."

def testRematch():
    deleteMatches()
    deletePlayers()
    deleteTournament()
    deleteScoreboard()
    Tid = createTournament('Test')
    registerPlayer("One", Tid)
    registerPlayer("Two", Tid)
    registerPlayer("Three", Tid)
    registerPlayer("Four", Tid)
    registerPlayer("Five", Tid)
    registerPlayer("Six", Tid)
    standings = playerStandings(Tid)
    [player_id1, player_id2, player_id3, player_id4, player_id5, player_id6] = [i[0] for i in standings]
    reportMatch(Tid, player_id1, player_id2)
    reportMatch(Tid, player_id3, player_id4)
    reportMatch(Tid, player_id5, player_id6)
    reportMatch(Tid, player_id1, player_id3)
    reportMatch(Tid, player_id5, player_id2)
    reportMatch(Tid, player_id4, player_id6)
    pairings = swissPairings(Tid)
    if len(pairings) != 3:
        raise ValueError("swissPairings() should return 3 pairs for 6 registered players.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6)] = pairings
    correct_pairs = set([frozenset([player_id1, player_id5]), frozenset([player_id3, player_id2]), frozenset([player_id4, player_id6])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6])])
    if correct_pairs != actual_pairs:
        raise ValueError("Rematch occurred(A match between same 2 players).")
    print "13. Rematch are not allowed"

if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testReportBye()
    testHasBye()
    testCheckByes()
    testPairings()
    testOddPairings()
    testRematch()
    print("Success!  All tests pass!")
