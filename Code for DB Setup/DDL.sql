--Relational Tables
create table BoxScore
(
    Game_id                              int not null primary key,
    team_id_home                         int,
    team_id_away                         int,
    Minutes_played                       int,
    Points_hometeam                      int,
    Points_away                          int,
    field_goal_attempts_home             int,
    field_goal_Made_home                 int,
    field_goal_attempts_away             int,
    field_goal_Made_away                 int,
    three_point_field_goal_attempts_home int,
    three_point_field_goal_attempts_away int,
    three_point_field_goal_made_home     int,
    three_point_field_goal_made_away     int,
    free_throw_attempts_Home             int,
    free_throw_attempts_away             int,
    free_throw_made_Home                 int,
    free_throw_made_away                 int,
    reb_away                             int,
    reb_home                             int,
    assist_home                          int,
    assist_away                          int,
    Steal_home                           int,
    Steal_away                           int,
    Pf_away                              int,
    Pf_home                              int,
    Blocked_shots_away                   int,
    Blocked_shots_home                   int
)


create table Draft_history
(
    Person_id    int not null,
    Player_name  varchar(50),
    season       int not null,
    Round_number int,
    round_pick   int,
    team_id      int not null,
    primary key (Person_id, season, team_id)
)



create table Official
(
    Official_id int not null,
    Name        varchar(50),
    Game_id     int not null,
    Jerseynum   int,
    primary key (Official_id, Game_id)
)

--Graph Tables

create table GameDimention
(
    Game_ID                                     int not null primary key,
    Date                                        date,
    home_team_id                                int,
    away_team_id                                int,
    Season                                      varchar(50),
    Score                                       varchar(50)
) AS NODE


create table Player_Dimension
(
    Player_id                                   int not null primary key,
    PlayerName                                  varchar(50),
    Position                                    varchar(50),
    Height                                      varchar(10),
    Weight                                      int,
    Birthdate                                   date,
    College                                     varchar(50),
    Country                                     varchar(50),
    season_experience                           int,
    Jersey                                      int,
    from_year                                   int,
    to_year                                     int,
    nba_flag                                    varchar(5)
) AS NODE


create table Team
(
    TeamID                                      int not null primary key,
    TeamName                                    varchar(255),
    City                                        varchar(255),
    State                                       varchar(255),
    Arena                                       varchar(255),
    ArenaCapacity                               int,
    HeadCoach                                   varchar(255),
    Conference                                  varchar(255),
    TeamDivision                                varchar(255),
    YearFounded                                 int,
    Wins                                        int,
    Losses                                      int,
    PCT                                         decimal(5, 3),
    Division_Rank                               int
) AS NODE


CREATE TABLE plays_for AS EDGE;


CREATE TABLE plays_in (H_A varchar(10)) AS EDGE;


create table Player_Team_Bridge
(
    Player_id int,
    Team_id   int
)

--Document Table

create table PlayerDraftStatistics
(
    JsonData nvarchar(max)
)

-- Stored Procedures 

CREATE PROCEDURE usp_Insert_Plays_For
AS
BEGIN
    DROP TABLE plays_for
    CREATE TABLE plays_for AS EDGE
    INSERT INTO plays_for
    SELECT p.$node_id, t.$node_id
    FROM Player_dimension p
    INNER JOIN Player_Team_Bridge pt ON p.Player_id = pt.Player_id
    INNER JOIN Team t ON t.TeamID = pt.Team_id
END


CREATE PROCEDURE usp_Insert_Plays_In
AS
BEGIN
    DROP TABLE plays_in

    CREATE TABLE plays_in (H_A varchar(10)) AS EDGE

    INSERT INTO plays_in
    SELECT n1, n2, h_a
    FROM (
        SELECT t.$node_id n1, g_h.$node_id n2, 'Home' h_a
        FROM GameDimention g_h
        JOIN team t ON g_h.home_team_id = t.TeamID
        UNION
        SELECT t.$node_id, g_h.$node_id, 'Away'
        FROM GameDimention g_h
        JOIN team t ON g_h.away_team_id = t.TeamID
    ) a;
END


CREATE PROCEDURE JsonImport
AS
BEGIN

TRUNCATE TABLE [dbo].[PlayerDraftStatistics]
BULK INSERT [dbo].[PlayerDraftStatistics]
FROM 'documentdata/draft_combine_stats.json'
WITH ( DATA_SOURCE = 'MyAzureBlobStorage');

END
go




