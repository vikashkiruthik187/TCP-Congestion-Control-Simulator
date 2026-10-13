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
    def __init__(self, algorithm="Tahoe", initial_cwnd=1.0, initial_ssthresh=16.0):
        self.algorithm = algorithm
        self.cwnd = float(initial_cwnd)
        self.ssthresh = float(initial_ssthresh)
        self.state = "Slow Start" if self.cwnd < self.ssthresh else "Congestion Avoidance"
        
        # Cubic state variables (Linux standard)
        self.w_max = float(initial_ssthresh)
        self.epoch_start = 0
        self.c_constant = 0.4
        self.beta_cubic = 0.7  # Multiplicative decrease factor (30% drop vs Reno's 50%)
        self.k = 1.2
        self.current_tick = 0

    def update_on_ack(self, tick=0):
        self.current_tick = tick
        if self.cwnd < self.ssthresh:
            self.cwnd += 1.0  # Slow start (exponential)
            self.state = "Slow Start"
        else:
            if self.algorithm == "Cubic":
                # TCP Cubic: W_cubic(t) = C*(t - K)^3 + W_max
                t_elapsed = max(0.0, (self.current_tick - self.epoch_start) * 0.1)
                target_w = self.c_constant * ((t_elapsed - self.k) ** 3) + self.w_max
                inc = max(0.05, (target_w - self.cwnd) / max(1.0, self.cwnd))
                self.cwnd += min(1.8, inc)
                self.state = "Cubic Concave" if t_elapsed < self.k else "Cubic Convex"
            else:
                self.cwnd += 1.0 / self.cwnd  # Linear AIMD
                self.state = "Congestion Avoidance"

    def update_on_loss(self, tick=0):
        self.current_tick = tick
        if self.algorithm == "Tahoe":
            # Tahoe: Drop cwnd to 1, cut ssthresh
            self.ssthresh = max(2.0, self.cwnd / 2.0)
            self.cwnd = 1.0
            self.state = "Slow Start"
        elif self.algorithm == "Reno":
            # Reno: Fast recovery - cut cwnd in half
            self.ssthresh = max(2.0, self.cwnd / 2.0)
            self.cwnd = max(1.0, self.cwnd / 2.0)
            self.state = "Fast Recovery"
        elif self.algorithm == "Cubic":
            # Cubic: Drop by 30% instead of 50%, recalculate epoch and K
            self.w_max = max(2.0, self.cwnd)
            self.ssthresh = max(2.0, self.cwnd * self.beta_cubic)
            self.cwnd = self.ssthresh
            val = (self.w_max * (1.0 - self.beta_cubic)) / self.c_constant
            self.k = (val ** (1.0 / 3.0)) if val > 0 else 1.0
            self.epoch_start = self.current_tick
            self.state = "Cubic Recovery"

def calculate_jains_fairness(flow_throughputs):
    """
    Computes Jain's Fairness Index: J = (sum(x_i))^2 / (n * sum(x_i^2))
    Ranges from 1/n to 1.0 (perfect fairness).
    """
    n = len(flow_throughputs)
    if n == 0 or sum(flow_throughputs) == 0:
        return 1.0
    sum_x = sum(flow_throughputs)
    sum_x_sq = sum(x ** 2 for x in flow_throughputs)
    if sum_x_sq == 0:
        return 1.0
    return round((sum_x ** 2) / (n * sum_x_sq), 3)

def run_simulation(ticks=200, loss_rate=0.05, algorithm="Tahoe", initial_cwnd=1.0, initial_ssthresh=16.0, rwnd=64.0, bdp=32.0, seed=None):
    rng = random.Random(seed) if seed is not None else random.Random()
    sender = TCPSender(algorithm, initial_cwnd=initial_cwnd, initial_ssthresh=initial_ssthresh)
    results = []
    rwnd_val = float(rwnd)
    bdp_val = max(1.0, float(bdp))

    for t in range(ticks):
        packet_lost = rng.random() < loss_rate

        if packet_lost:
            sender.update_on_loss(tick=t)
            event = "Packet Loss"
        else:
            sender.update_on_ack(tick=t)
            event = "ACK"

        effective_w = min(sender.cwnd, rwnd_val)
        utilization = min(effective_w, bdp_val) / bdp_val * 100.0
        queued = max(0.0, effective_w - bdp_val)
        limiting_factor = "Flow Control (rwnd)" if sender.cwnd >= rwnd_val else "Congestion (cwnd)"

        results.append({
            "Tick": t,
            "CongestionWindow": round(sender.cwnd, 2),
            "ReceiverWindow": round(rwnd_val, 2),
            "EffectiveWindow": round(effective_w, 2),
            "Ssthresh": round(sender.ssthresh, 2),
            "Event": event,
            "Loss": packet_lost,
            "Phase": sender.state,
            "LinkUtilization": round(utilization, 1),
            "QueuedPackets": round(queued, 2),
            "LimitingFactor": limiting_factor
        })
    return results
if __name__ == "__main__":
    # Run a quick test simulation for 50 ticks
    sim_results = run_simulation(ticks=50, loss_rate=0.05, algorithm="Tahoe")
    
    print("Tick | Congestion Window (cwnd) | Ssthresh")
    print("-" * 45)
    for row in sim_results[:20]:  # Print the first 20 ticks
        print(f"{row['Tick']:4d} | {row['CongestionWindow']:24.2f} | {row['Ssthresh']:8.2f}")