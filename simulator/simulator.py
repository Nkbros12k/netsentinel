"""Traffic simulator — generates mixed normal/attack flows and sends to API."""

import argparse
import time
import random
import requests
from profiles import generate_flow


def run(api_url: str, rate: float, attack_ratio: float):
    print(f"NetSentinel Simulator")
    print(f"  Target:       {api_url}")
    print(f"  Rate:         {rate} req/s")
    print(f"  Attack ratio: {attack_ratio:.0%}")
    print()

    total = 0
    threats = 0

    while True:
        flow = generate_flow(attack_ratio)
        try:
            resp = requests.post(f"{api_url}/predict", json=flow, timeout=5)
            result = resp.json()
            total += 1
            label = result.get("prediction", "?")
            conf = result.get("confidence", 0)
            level = result.get("threat_level", "?")

            if label != "Normal":
                threats += 1
                print(f"  [{total:>5}] THREAT  {label:<8} conf={conf:.2f}  level={level}")
            elif total % 10 == 0:
                print(f"  [{total:>5}] normal  (threats so far: {threats})")

        except requests.RequestException as e:
            print(f"  [{total:>5}] ERROR: {e}")

        delay = 1.0 / rate + random.uniform(-0.1, 0.1)
        time.sleep(max(0.05, delay))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NetSentinel Traffic Simulator")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--rate", type=float, default=2.0, help="Requests per second")
    parser.add_argument("--attack-ratio", type=float, default=0.3, help="Fraction of attack traffic")
    args = parser.parse_args()
    run(args.api_url, args.rate, args.attack_ratio)
