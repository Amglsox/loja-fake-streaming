x=1
while [ $x -le 2000000 ]
do
  curl http://localhost:9090/shopping/create
  echo $x
  x=$(( $x + 1 ))
done
