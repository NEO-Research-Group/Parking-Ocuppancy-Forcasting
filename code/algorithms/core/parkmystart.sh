#!/bin/bash

intervals=(30) 
city="birmingham" #"malaga" #"birmingham" #"malaga" "birmingham" 
algorithms=("neural_prophet") #("sarimax") #("neural_prophet") # "prophet" "sarimax" "neural_prophet" "LSTM" "SimpleRNN" "GRU"): 
parkings=('Shopping')
#('BHMNCPPLS01' 'BHMBCCMKT01' 'BHMBCCPST01' 'BHMBCCSNH01' 'BHMBCCTHL01'
# 'BHMBRCBRG01' 'BHMBRCBRG02' 'BHMBRCBRG03' 'BHMEURBRD01' 'BHMEURBRD02'
# 'BHMMBMMBX01' 'BHMNCPHST01' 'BHMNCPLDH01' 'BHMNCPNHS01' 'BHMNCPNST01'
# 'BHMNCPRAN01' 'Broad Street' 'Bull Ring' 'NIA Car Parks' 'NIA South'
# 'Others-CCCPS105a' 'Others-CCCPS119a' 'Others-CCCPS133'
# 'Others-CCCPS135a' 'Others-CCCPS202' 'Others-CCCPS8' 'Others-CCCPS98'
# 'Shopping')
#("Salitre")
#('BHMNCPPLS01' 'BHMBCCMKT01' 'BHMBCCPST01' 'BHMBCCSNH01' 'BHMBCCTHL01'
# 'BHMBRCBRG01' 'BHMBRCBRG02' 'BHMBRCBRG03' 'BHMEURBRD01' 'BHMEURBRD02'
# 'BHMMBMMBX01' 'BHMNCPHST01' 'BHMNCPLDH01' 'BHMNCPNHS01' 'BHMNCPNST01'
# 'BHMNCPRAN01' 'Broad Street' 'Bull Ring' 'NIA Car Parks' 'NIA South'
# 'Others-CCCPS105a' 'Others-CCCPS119a' 'Others-CCCPS133'
# 'Others-CCCPS135a' 'Others-CCCPS202' 'Others-CCCPS8' 'Others-CCCPS98'
# 'Shopping') #("BHMBCCMKT01") #("Salitre" "San Juan De La Cruz" "Cruz De Humilladero") #("Salitre" "Cruz De Humilladero" "San Juan De La Cruz") # "Cruz De Humilladero" "San Juan De La Cruz") #"San Juan De La Cruz" "Cruz De Humilladero") 
day_of_the_week=(0) #(0 1 2 3 4 5 6) #(0 1 2 3 4 5 6)  #(0 1 2 3 4 5 6) 
holidays=(0) #(0 1)
cross_validation=('week') # 'week' 'twoweeks' 'threeweeks' 'month' #4)  #(0 1 2 3 4) 
window_size=18 #48 #18



for interval in "${intervals[@]}"
do
  for alg in "${algorithms[@]}"
  do
    for par in "${parkings[@]}"
    do
      for dow in "${day_of_the_week[@]}"
      do
        for hol in "${holidays[@]}"
        do
          for cv in "${cross_validation[@]}"
          do
            echo $alg
            echo $par
            echo $dow
            echo $hol
            echo $cv 
            echo "-i ${interval} -a ${alg} -p "${par}" -d ${dow} -ho ${hol} -v ${cv} -c ${city}"                                       
            nohup python run.py -i ${interval} -a ${alg} -p "${par}" -d ${dow} -ho ${hol} -v ${cv} -c ${city} -w ${window_size} > output"${par}"holi"${hol}"dow"${dow}"alg"${alg}".txt &

          done
        done
      done
    done
  done
done
