cat clients/client1_error.txt | netcat -i 1 -w 1 0.0 8090 > client1.txt
sleep 1
out=`diff -w client1.txt output/client_error.out`
if [ "$out" == "" ]
then
    tput setaf 2; echo "PASSED client_error"
    echo -e '\t{ "client_error" : "Passed" },' >> tests.json
else
    tput setaf 1; echo "FAILED client_error"
    echo -e '\t{ "client_error" : "Failed" },' >> tests.json
fi
tput sgr0