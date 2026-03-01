#!/bin/bash
# nc-wrapper.sh
# Usage: ./nc-wrapper.sh <host> [netconf-console2 options...]

# ─── Credential Store ─────────────────────────────────────────────────────────
# Format: HOST|PORT|USERNAME|PASSWORD
CREDENTIALS=(
    "192.168.100.11|830|admin|admin"
    "ceos-01|830|admin|admin"
    "srl-01|830|admin|NokiaSrl1!"
    "192.168.100.12|830|admin|NokiaSrl1!"
    "srl-02|803|admin|NokiaSrl1!"
    "192.168.100.13|830|admin|NokiaSrl1!"
)

# ─── Credential lookup ────────────────────────────────────────────────────────
TARGET_HOST="$1"
shift

for entry in "${CREDENTIALS[@]}"; do
    IFS='|' read -r h p u pw <<< "$entry"
    if [[ "$h" == "$TARGET_HOST" ]]; then
        netconf-console2 --host "$h" --port "$p" -u "$u" -p "$pw" "$@"
        exit $?
    fi
done

echo "Error: No credentials found for host '$TARGET_HOST'"
exit 1
