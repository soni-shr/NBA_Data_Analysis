
-- Graph Query 
SELECT t.TeamName, g.Game_ID, g.Season, plays_in.H_A
FROM Team t, plays_in, GameDimention g
WHERE MATCH(t-(plays_in)->g)
and t.TeamName = 'Lakers'
and plays_in.H_A = 'Away'
;

SELECT p.PlayerName, t.TeamName
FROM Player_dimension p, plays_for, Team t
WHERE MATCH(p-(plays_for)->t)
and t.TeamName = 'Lakers';

--Document Query

SELECT JSON_VALUE(JsonData, '$[0].player_id') AS Id,
       JSON_VALUE(JsonData, '$[0].position') AS Name,
       JSON_VALUE(JsonData, '$[0].weight') AS Weight
FROM PlayerDraftStatistics;