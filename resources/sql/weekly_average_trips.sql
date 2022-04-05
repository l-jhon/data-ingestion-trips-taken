SELECT tb.region ,
       avg(weekly)
FROM
  (SELECT region ,
          extract(WEEK
                  FROM datetime) ,
          count(*) AS weekly
   FROM trips
   GROUP BY 1,
            2) AS tb
GROUP BY 1