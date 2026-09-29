import random

class Packet:
    def __init__(self, seq_num, send_time):
        self.seq_num = seq_num
        self.send_time = send_time

class NetworkLink:
    def __init__(self, bandwidth_pps, propagation_delay_ticks, buffer_size):
        self.bandwidth_pps = bandwidth_pps  # Packets per tick allowed
        self.propagation_delay = propagation_delay_ticks  # Ticks to travel
        self.buffer_size = buffer_size  # Max packets in router queue
        self.queue = []
        self.in_flight_to_receiver = []
        self.ack_queue = []

    def send_packet(self, pkt):
        if len(self.queue) < self.buffer_size:
            self.queue.append(pkt)
            return True  # Successfully queued
        return False  # Packet dropped (Buffer overflow)

    def tick(self, current_tick):
        # Process router queue to link
        # Simplified: Move packets forward based on bandwidth & delay
        pass

class TCPSender:
    def __init__(self, algorithm="Tahoe"):
        self.algorithm = algorithm
        self.cwnd = 1.0
        self.ssthresh = 16.0

    def update_on_ack(self):
        if self.cwnd < self.ssthresh:
            self.cwnd += 1.0  # Slow start (exponential-ish)
        else:
            self.cwnd += 1.0 / self.cwnd  # Congestion avoidance (linear)

    def update_on_loss(self):
        if self.algorithm == "Tahoe":
            # Tahoe: Drop cwnd to 1, cut ssthresh
            self.ssthresh = max(2.0, self.cwnd / 2.0)
            self.cwnd = 1.0
        elif self.algorithm == "Reno":
            # Reno: Fast recovery - cut cwnd and ssthresh in half, don't drop to 1
            self.ssthresh = max(2.0, self.cwnd / 2.0)
            self.cwnd = max(1.0, self.cwnd / 2.0)

def run_simulation(ticks=200, loss_rate=0.05, algorithm="Tahoe"):
    sender = TCPSender(algorithm)
    results = []

    for t in range(ticks):
        packet_lost = random.random() < loss_rate

        if packet_lost:
            sender.update_on_loss()
        else:
            sender.update_on_ack()

        results.append({
            "Tick": t,
            "CongestionWindow": sender.cwnd,
            "Ssthresh": sender.ssthresh
        })
    return results
if __name__ == "__main__":
    # Run a quick test simulation for 50 ticks
    sim_results = run_simulation(ticks=50, loss_rate=0.05, algorithm="Tahoe")
    
    print("Tick | Congestion Window (cwnd) | Ssthresh")
    print("-" * 45)
    for row in sim_results[:20]:  # Print the first 20 ticks
        print(f"{row['Tick']:4d} | {row['CongestionWindow']:24.2f} | {row['Ssthresh']:8.2f}")