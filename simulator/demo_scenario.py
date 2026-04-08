"""Demo scenario — starts calm, then escalates into a massive global attack wave."""

import time
import random
import requests
from profiles import normal_flow, dos_flow, probe_flow, r2l_flow, u2r_flow

API_URL = "http://localhost:8000"


def send(flow):
    try:
        resp = requests.post(f"{API_URL}/predict", json=flow, timeout=5)
        result = resp.json()
        label = result.get("prediction", "?")
        conf = result.get("confidence", 0)
        level = result.get("threat_level", "?")
        if label != "Normal":
            print(f"  THREAT  {label:<8} conf={conf:.2f}  level={level}")
        return result
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def phase_normal(duration=20):
    """Phase 1: Calm, normal traffic."""
    print("\n" + "=" * 60)
    print("PHASE 1: Normal Operations")
    print("Routine network traffic, no anomalies detected...")
    print("=" * 60)
    end = time.time() + duration
    count = 0
    while time.time() < end:
        send(normal_flow())
        count += 1
        if count % 5 == 0:
            print(f"  [{count}] all clear...")
        time.sleep(random.uniform(0.3, 0.6))


def phase_recon(duration=15):
    """Phase 2: Reconnaissance — probing starts appearing."""
    print("\n" + "=" * 60)
    print("PHASE 2: Reconnaissance Detected")
    print("Port scans and network probes from multiple sources...")
    print("=" * 60)
    end = time.time() + duration
    while time.time() < end:
        if random.random() < 0.4:
            send(probe_flow())
        else:
            send(normal_flow())
        time.sleep(random.uniform(0.2, 0.5))


def phase_escalation(duration=15):
    """Phase 3: Escalation — mixed attacks increase."""
    print("\n" + "=" * 60)
    print("PHASE 3: Attack Escalation")
    print("Multiple attack vectors detected, threat level rising...")
    print("=" * 60)
    end = time.time() + duration
    while time.time() < end:
        r = random.random()
        if r < 0.3:
            send(dos_flow())
        elif r < 0.5:
            send(probe_flow())
        elif r < 0.6:
            send(r2l_flow())
        else:
            send(normal_flow())
        time.sleep(random.uniform(0.15, 0.4))


def phase_full_attack(duration=25):
    """Phase 4: Full-scale coordinated attack — massive spike."""
    print("\n" + "=" * 60)
    print("PHASE 4: FULL-SCALE ATTACK")
    print("Coordinated DDoS from global botnet! All systems under siege!")
    print("=" * 60)
    end = time.time() + duration
    while time.time() < end:
        # Burst: send 3-5 attacks rapidly
        burst = random.randint(3, 6)
        for _ in range(burst):
            r = random.random()
            if r < 0.5:
                send(dos_flow())
            elif r < 0.7:
                send(probe_flow())
            elif r < 0.85:
                send(r2l_flow())
            else:
                send(u2r_flow())
            time.sleep(random.uniform(0.05, 0.15))
        # Brief pause between bursts
        time.sleep(random.uniform(0.1, 0.3))


def phase_aftermath(duration=15):
    """Phase 5: Attack subsides, returning to normal."""
    print("\n" + "=" * 60)
    print("PHASE 5: Attack Subsiding")
    print("Threat levels decreasing, returning to normal operations...")
    print("=" * 60)
    end = time.time() + duration
    attack_chance = 0.3
    while time.time() < end:
        if random.random() < attack_chance:
            send(random.choice([dos_flow, probe_flow])())
        else:
            send(normal_flow())
        attack_chance -= 0.01
        attack_chance = max(0.05, attack_chance)
        time.sleep(random.uniform(0.3, 0.6))

    print("\n" + "=" * 60)
    print("SCENARIO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    print("NetSentinel Demo Scenario")
    print("Watch the dashboard at http://localhost:5173")
    print("Starting in 3 seconds...")
    time.sleep(3)

    phase_normal(20)
    phase_recon(15)
    phase_escalation(15)
    phase_full_attack(25)
    phase_aftermath(15)
