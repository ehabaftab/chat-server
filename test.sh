bash tests/start_server.sh
sleep 1
bash tests/client_register.sh
bash tests/client_login.sh
bash tests/client_login_error.sh
bash tests/client_error.sh
bash tests/client_error2.sh
bash tests/multiple_clients_login.sh
bash tests/multiple_clients_chat.sh
bash tests/stop_server.sh
tput setaf 2; echo "DONE"
tput sgr0