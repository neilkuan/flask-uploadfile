x=1
while [ $x -eq 1  ]
do
   curl http://localhost:8080/ping
   sleep 1
done
