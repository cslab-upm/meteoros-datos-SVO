#!/bin/bash
for ((c=$3; c<=$4; c++))
do
        if [[ $c -gt 9 ]];
        then
                echo "Ejecutando programa ./meteoros.sh $1 $2-$c"
                ./meteoros.sh $1 $2-$c
                echo "$2-$c terminado"
        else
                echo "Ejecutando programa ./meteoros.sh $1 $2-0$c"
                ./meteoros.sh $1 $2-0$c
                echo "$2-0$c terminado"
        fi
done

