cat clients/client1_error2.txt | netcat -i 1 -w 1 0.0 8090 > client1.txt
sleep 3
out=`diff -w client1.txt output/client_error2.out`
if [ "$out" == "" ]
then
    tput setaf 2; echo "PASSED client_error2"
    echo -e '\t{ "client_error2" : "Passed" },' >> tests.json
else
    tput setaf 1; echo "FAILED client_error"
    echo -e '\t{ "client_error2" : "Failed" },' >> tests.json
fi
tput sgr0