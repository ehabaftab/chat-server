cat clients/client1_register.txt | netcat -i 1 -w 1 0.0 8090 > client1.txt
sleep 1
out=`diff -w client1.txt output/client_register.out`
if [ "$out" == "" ]
then
    tput setaf 2; echo "PASSED client_register"
    echo -e '[\n\t{ "client_register" : "Passed" },' > tests.json
else
    tput setaf 1; echo "FAILED client_register"
    echo -e '[\n\t{ "client_register" : "Failed" },' > tests.json
fi
tput sgr0