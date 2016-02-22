-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- Wins View shows number of wins for each Player
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Tournament;
DROP TABLE IF EXISTS scoreboard;

-- Players Table
CREATE TABLE Players
(
	player_id SERIAL primary key,
	player_name varchar(255)
);

---Tournament Table--
CREATE TABLE Tournament
(
	tournament_id serial ,
	tournament_desc varchar(255)
);

-- Matches Table
CREATE TABLE Matches
(
	match_id SERIAL primary key,
  tournament_id int ,
	winner_id int references Players(player_id) on Delete Cascade,
	losser_id int references Players(player_id) on Delete Cascade,
  draw boolean
	--result int
);

--scoreboard table
--tournament_id, player_id, scores, num_matches, num_byes
CREATE TABLE Scoreboard ( tournament_id INT,
                          player_id INT,
                          score INT,
                          num_matches INT,
                          num_bye INT );
