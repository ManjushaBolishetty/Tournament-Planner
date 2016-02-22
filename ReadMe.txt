Files

Following are the list of code files available to the user.
1. tournament.py -- python code implementing Swiss-pair tournament
2. tournament.sql --table structure for the swiss pair project, Queries to fetch the reuired data.
3. tournament_test.py -- Test cases for tournament.py

How to implement
Ensure database tournament exists

1. Execute vagrant up - Ensure the Virtual Machine is up and running.
2. Execute vagrant ssh - ensure the execution is secure
3. Type psql in the command prompt
4. CREATE DATABASE tournament;
5. \c tournament - to connect to the database just created in the previous step
6. psql tournament < tournament.sql - Execute all the SQL statements in the tournament.sql file
by import the .sql file or type in individual SQL statements followed by a semicolon
6. Run some select statements to verify the tables are created.
7. \q to exit from the database when required.
8. Type "help" for help between any step if required to seek built-in help.
9. run python tournament_test.py from the path where the tournament_test.py is stored in the unix box.
10. Following are sequence of steps in tournament_test.py
a. Old matches can be deleted.
b. Player records can be deleted.
c. After deleting, countPlayers() returns zero.
d. After registering a player, countPlayers() returns 1.
e. Players can be registered and deleted.
f. Newly registered players appear in the standings with no matches.
g. After a match, players have updated standings.
h. All Byes are reported
i. Byes are validated
j. Byes are assigned properly
k. After one match, players with one win are paired.
l. With odd number, last player should have bye.
m. Rematch avoided.
Success!  All tests pass!
