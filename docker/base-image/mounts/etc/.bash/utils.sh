#!/usr/bin/env bash

# set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
GRAY='\033[0;30m'
MAGENTA='\033[0;35m'

# set timezone to Asia/Riyadh - !requires root privileges
# ln -sf /usr/share/zoneinfo/Asia/Riyadh /etc/localtime
# echo "Asia/Riyadh" > /etc/timezone

safe_exec() {
    local cmd="$1"
    local default="${2:-N/A}"
    local result
    result=$(${cmd} 2>/dev/null) || echo "$default"
    echo "$result"
}

SYSTEM_NAME=$(cat /etc/os-release | grep "NAME" | awk 'NR==2 {print $1}' | cut -d '=' -f 2 | tr -d '"')
SYSTEM_VERSION=$(cat /etc/os-release | grep 'VERSION_ID' | awk -F'=' '{print $2}' | tr -d '"')
SYSTEM_ARCH=$(uname -m)
SYSTEM_USER=$(whoami)
SYSTEM_GROUP=$(id -gn)
SYSTEM_HOME=$(eval echo "~${SYSTEM_USER}")
# SYSTEM_HOME=$(eval echo "~${SYSTEM_USER}")
# SYSTEM_SHELL=$(eval echo "${SYSTEM_USER}/.bashrc")
# SYSTEM_EDITOR=$(eval echo "${SYSTEM_USER}/.editorconfig")
# SYSTEM_CONFIG=$(eval echo "${SYSTEM_USER}/.config")
# SYSTEM_CACHE=$(eval echo "${SYSTEM_USER}/.cache")
# SYSTEM_DATA=$(eval echo "${SYSTEM_USER}/.local/share")
# SYSTEM_LOG=$(eval echo "${SYSTEM_USER}/.log")
# SYSTEM_TEMP=$(eval echo "${SYSTEM_USER}/.temp")
# SYSTEM_TMP=$(eval echo "${SYSTEM_USER}/.tmp")
# SYSTEM_VAR=$(eval echo "${SYSTEM_USER}/.var")
# SYSTEM_XDG_DATA_HOME=$(eval echo "${SYSTEM_USER}/.local/share")
# SYSTEM_XDG_CONFIG_HOME=$(eval echo "${SYSTEM_USER}/.config")
# SYSTEM_XDG_CACHE_HOME=$(eval echo "${SYSTEM_USER}/.cache")
SYSTEM_INFO_DATE="$(date)"
SYSTEM_UPTIME=$(safe_exec "/usr/bin/uptime -p" "N/A")
SYSTEM_LOAD="$(uptime | awk -F'load average: ' '{print $2}' | awk -F, '{printf "%%%.2f", $3}')"
SYSTEM_LOAD_PERCENT="$(uptime | awk -v cores=$(nproc) -F'load average: ' '{split($2, a, ","); printf "%%%.2f\n", (a[3] / cores) * 100}')"
PROCESSES="$(ls /proc | grep -E '^[0-9]+$' | wc -l)"
CORES="$(nproc)"
USAGE_OF_DISK="$(df -h / | awk 'NR==2 {print $5}')"
TOTAL_DISK="$(df -h / | awk 'NR==2 {print $2}')"
USERS_LOGGED_IN="$(who | wc -l)"
MEMORY_USAGE="$(free -m | awk 'NR==2 {pct=$3/$2*100; printf "%.0f%% of %.1fGB (%.1fGB used / %.1fGB free)\n", pct, $2/1024, $3/1024, $7/1024}')"
SWAP_USAGE="$(free -m | awk 'NR==3 {pct=$3/$2*100; printf "%.0f%% of %.1fGB (%.1fGB used / %.1fGB free)\n", pct, $2/1024, $3/1024, $4/1024}')"
IP_ADDRESS="$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d '/' -f 1)"
LOCAL_IP_ADDRESS="$(ip addr show lo | grep 'inet ' | awk 'NR==1 {print $2}' | cut -d '/' -f 1)"
# check if /etc/timezone exists and is not empty
if [ -s /etc/timezone ]; then
    TIMEZONE="$(cat /etc/timezone)"
else
    TIMEZONE='UTC'
fi
APP_ENV=${APP_ENV:-'development'}
APP_VERSION=$APP_VERSION
APP_NAME='Experts App'

echo -e "${BLUE}$(cat /etc/.bash/ascii.art)${NC}"

echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ '
echo ''
echo " $APP_NAME v$APP_VERSION - $APP_ENV | by Logix, Inc.         "
echo ''
echo '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ '
echo ''

# cat <<EOF
# $(/opt/go/bin/healthcheck | while read line; do
#     if [[ $line == *"OK"* ]]; then
#         echo -e "${GREEN}$line${NC}"
#     elif [[ $line == *"MISSING (optional)"* ]]; then
#         echo -e "${YELLOW}$line${NC}"
#     else
#         echo -e "${RED}$line${BOLD}"
#     fi
# done)

# EOF
echo -e "System information as of ${WHITE}$SYSTEM_INFO_DATE${NC}"
printf " %-25s ${BLUE}%s${NC}\n" "OS:" "$SYSTEM_NAME $SYSTEM_VERSION"
printf " %-25s ${BLUE}%s${NC}\n" "Uptime:" "$SYSTEM_UPTIME"
printf " %-25s ${BLUE}%s${NC}\n" "Architecture:" "$SYSTEM_ARCH"
printf " %-25s ${BLUE}%s${NC}\n" "User:" "$SYSTEM_USER"
printf " %-25s ${BLUE}%s${NC}\n" "Group:" "$SYSTEM_GROUP"
printf " %-25s ${BLUE}%s${NC}\n" "Home:" "$SYSTEM_HOME"
printf " %-25s ${BLUE}%s${NC}\n" "System load:" "$SYSTEM_LOAD"
printf " %-25s ${BLUE}%s${NC}\n" "Processes:" "$PROCESSES"
printf " %-25s ${BLUE}%s${NC}\n" "Cores:" "$CORES"
printf " %-25s ${BLUE}%s${NC}\n" "Load Percent:" "$SYSTEM_LOAD_PERCENT"
printf " %-25s ${BLUE}%s${NC}\n" "Usage of /:" "$USAGE_OF_DISK"
printf " %-25s ${BLUE}%s${NC}\n" "Total Disk:" "$TOTAL_DISK"
printf " %-25s ${BLUE}%s${NC}\n" "Users logged in:" "$USERS_LOGGED_IN"
printf " %-25s ${BLUE}%s${NC}\n" "Memory usage:" "$MEMORY_USAGE"
printf " %-25s ${BLUE}%s${NC}\n" "Swap usage:" "$SWAP_USAGE"
printf " %-25s ${BLUE}%s${NC}\n" "IPv4 address for eth0:" "$IP_ADDRESS"
printf " %-25s ${BLUE}%s${NC}\n" "IPv4 address for lo:" "$LOCAL_IP_ADDRESS"
printf " %-25s ${BLUE}%s${NC}\n" "Timezone:" "$TIMEZONE"
echo ''
