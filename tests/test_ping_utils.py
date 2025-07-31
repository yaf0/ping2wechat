from ping_utils import parse_loss_rate, parse_avg_latency

def test_parse_loss_rate():
    output = "64 bytes from 8.8.8.8: icmp_seq=1 ttl=57 time=30.4 ms\n--- 8.8.8.8 ping statistics ---\n1 packets transmitted, 1 received, 0% packet loss, time 0ms"
    assert parse_loss_rate(output) == 0

def test_parse_avg_latency():
    output = "rtt min/avg/max/mdev = 30.450/30.450/30.450/0.000 ms"
    assert parse_avg_latency(output) == 30.45

