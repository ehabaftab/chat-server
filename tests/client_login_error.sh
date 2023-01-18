cat clients/client1_login_error.txt | netcat -i 1 -w 1 0.0 8090 > client1.txt
sleep 1
out=`diff -w client1.txt output/client_login_error.out`
if [ "$out" == "" ]
then
    tput setaf 2; echo "PASSED client_login_error"
    echo -e '\t{ "client_login_error" : "Passed" },' >> tests.json
else
    tput setaf 1; echo "FAILED client_login_error"
    echo -e '\t{ "client_login_error" : "Failed" },' >> tests.json
fi
tput sgr0