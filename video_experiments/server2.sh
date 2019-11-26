sudo iptables -t nat -A PREROUTING -p tcp -i ingress --dport 80 -j DNAT --to-destination 100.64.0.4:80
sudo iptables -A FORWARD -p tcp -d 100.64.0.4 --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
pathtolink=pensieve/rl_server
mm-link $pathtolink/100Mbps_trace $pathtolink/100Mbps_trace --meter-uplink
