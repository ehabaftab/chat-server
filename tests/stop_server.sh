PID=`cat pid`
kill -INT $PID
coverage report -m