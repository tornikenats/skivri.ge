red=$'\e[1;31m'
grn=$'\e[1;32m'
yel=$'\e[1;33m'
blu=$'\e[1;34m'
mag=$'\e[1;35m'
cyn=$'\e[1;36m'
end=$'\e[0m'

printf "${grn}Running webpack${end}\n"
cd application && yarn run webpack

printf "${grn}Building container${end}\n"
docker-compose build

printf "${grn}Running container${end}\n"
docker-compose up -d
