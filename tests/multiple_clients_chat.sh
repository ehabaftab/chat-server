cat clients/client1_say.txt | netcat -i 1 -w 1 0.0 8090 > client1.txt &
cat clients/client2_say.txt | netcat -i 1 -w 1 0.0 8090 > client2.txt &
sleep 8
out=`diff -w client1.txt output/client1_say.out`
out2=`diff -w client2.txt output/client2_say.out`
if [ "$out" == "" ] && [ "$out2" == "" ]
then
    tput setaf 2; echo "PASSED multiple_clients_chat"
    echo -e '\t{ " multiple_clients_chat" : "Passed" }\n]' >> tests.json
else
    tput setaf 1; echo "FAILED multiple_clients_chat"
    echo -e '\t{ " multiple_clients_chat" : "Failed" }\n]' >> tests.json
fi
tput sgr0