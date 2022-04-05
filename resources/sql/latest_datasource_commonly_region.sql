SELECT region,
       datasource
FROM
  (SELECT region ,
          datasource ,
          datetime ,
          row_number() over(PARTITION BY region
                            ORDER BY datetime DESC) rownum
   FROM trips
   WHERE region in
       (SELECT region
        FROM
          (SELECT DISTINCT region,
                           count(1)
           FROM trips
           GROUP BY 1
           ORDER BY 1 DESC
           LIMIT 2) AS tb)) AS tb2
WHERE rownum = 1