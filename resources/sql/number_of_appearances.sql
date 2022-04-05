SELECT region,
       datasource,
       count(1) number_of_appearances
FROM trips
WHERE datasource = 'cheap_mobile'
GROUP BY 1,
         2
ORDER BY 3 DESC