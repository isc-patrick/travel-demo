set -m

echo "Hello from init.sh"

iris session iris -U%SYS '##class(Security.Users).UnExpireUserPasswords("*")'

iris session iris -U%SYS '##class($SYSTEM.OBJ).LoadDir("/opt/irisapp/src/", "ck")'
 	
# iris session iris << EOF
# zpm
# install webterminal
# quit

# EOF