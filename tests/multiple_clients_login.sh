cat clients/client1_login.txt | netcat -i 1 -w 1 0.0 8090 > client1.txt
cat clients/client2_login.txt | netcat -i 1 -w 1 0.0 8090 > client2.txt
sleep 1
out=`diff -w client1.txt output/client_login.out`
out2=`diff -w client2.txt output/client2_login.out`
if [ "$out" == "" ]
then
    tput setaf 2; echo "PASSED multiple_clients_login"
    echo -e '\t{ " multiple_clients_login" : "Passed" },' >> tests.json
else
    tput setaf 1; echo "FAILED multiple_clients_login"
    echo -e '\t{ " multiple_clients_login" : "Failed" },' >> tests.json
fi
tput sgr0