sudo service apache2 stop
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A PREROUTING -p tcp -i enp3s0 --dport 80 -j DNAT --to-destination 100.64.0.2:80
sudo iptables -A FORWARD -p tcp -d 100.64.0.2 --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
mm-delay 40
