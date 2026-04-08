"""Attack traffic profiles derived from NSL-KDD distributions."""

import random

PROTOCOLS = ["tcp", "udp", "icmp"]
SERVICES = ["http", "smtp", "ftp", "ftp_data", "telnet", "private", "domain_u", "eco_i", "ecr_i", "other"]
FLAGS = ["SF", "S0", "REJ", "RSTR", "RSTO", "SH", "S1", "S2", "S3", "OTH"]


def normal_flow() -> dict:
    return {
        "duration": random.randint(0, 2000),
        "protocol_type": random.choice(["tcp", "udp"]),
        "service": random.choice(["http", "smtp", "ftp", "private", "other"]),
        "flag": "SF",
        "src_bytes": random.randint(100, 5000),
        "dst_bytes": random.randint(100, 10000),
        "land": 0,
        "wrong_fragment": 0,
        "urgent": 0,
        "hot": random.randint(0, 2),
        "num_failed_logins": 0,
        "logged_in": 1,
        "num_compromised": 0,
        "root_shell": 0,
        "su_attempted": 0,
        "num_root": 0,
        "num_file_creations": 0,
        "num_shells": 0,
        "num_access_files": 0,
        "num_outbound_cmds": 0,
        "is_host_login": 0,
        "is_guest_login": 0,
        "count": random.randint(1, 50),
        "srv_count": random.randint(1, 50),
        "serror_rate": round(random.uniform(0, 0.1), 2),
        "srv_serror_rate": round(random.uniform(0, 0.1), 2),
        "rerror_rate": round(random.uniform(0, 0.1), 2),
        "srv_rerror_rate": round(random.uniform(0, 0.1), 2),
        "same_srv_rate": round(random.uniform(0.8, 1.0), 2),
        "diff_srv_rate": round(random.uniform(0, 0.2), 2),
        "srv_diff_host_rate": round(random.uniform(0, 0.1), 2),
        "dst_host_count": random.randint(1, 255),
        "dst_host_srv_count": random.randint(1, 255),
        "dst_host_same_srv_rate": round(random.uniform(0.5, 1.0), 2),
        "dst_host_diff_srv_rate": round(random.uniform(0, 0.3), 2),
        "dst_host_same_src_port_rate": round(random.uniform(0, 0.5), 2),
        "dst_host_srv_diff_host_rate": round(random.uniform(0, 0.1), 2),
        "dst_host_serror_rate": round(random.uniform(0, 0.1), 2),
        "dst_host_srv_serror_rate": round(random.uniform(0, 0.1), 2),
        "dst_host_rerror_rate": round(random.uniform(0, 0.1), 2),
        "dst_host_srv_rerror_rate": round(random.uniform(0, 0.1), 2),
    }


def dos_flow() -> dict:
    flow = normal_flow()
    flow.update({
        "duration": 0,
        "protocol_type": random.choice(["tcp", "icmp"]),
        "service": random.choice(["http", "ecr_i", "private", "eco_i"]),
        "flag": random.choice(["SF", "S0", "REJ"]),
        "src_bytes": random.randint(0, 100),
        "dst_bytes": 0,
        "count": random.randint(100, 511),
        "srv_count": random.randint(100, 511),
        "same_srv_rate": 1.0,
        "diff_srv_rate": 0.0,
        "serror_rate": round(random.uniform(0.8, 1.0), 2),
        "srv_serror_rate": round(random.uniform(0.8, 1.0), 2),
        "dst_host_count": 255,
        "dst_host_srv_count": random.randint(1, 30),
        "dst_host_serror_rate": round(random.uniform(0.8, 1.0), 2),
        "dst_host_srv_serror_rate": round(random.uniform(0.8, 1.0), 2),
    })
    return flow


def probe_flow() -> dict:
    flow = normal_flow()
    flow.update({
        "duration": 0,
        "protocol_type": random.choice(["tcp", "icmp", "udp"]),
        "service": random.choice(["private", "other", "eco_i", "ecr_i"]),
        "flag": random.choice(["SF", "S0", "REJ", "RSTR"]),
        "src_bytes": random.randint(0, 500),
        "dst_bytes": 0,
        "logged_in": 0,
        "count": random.randint(1, 30),
        "srv_count": random.randint(1, 10),
        "same_srv_rate": round(random.uniform(0, 0.3), 2),
        "diff_srv_rate": round(random.uniform(0.5, 1.0), 2),
        "dst_host_count": random.randint(200, 255),
        "dst_host_diff_srv_rate": round(random.uniform(0.5, 1.0), 2),
        "dst_host_same_src_port_rate": round(random.uniform(0, 0.1), 2),
    })
    return flow


def r2l_flow() -> dict:
    flow = normal_flow()
    flow.update({
        "duration": random.randint(0, 500),
        "protocol_type": "tcp",
        "service": random.choice(["ftp", "telnet", "smtp", "http", "ftp_data"]),
        "flag": "SF",
        "src_bytes": random.randint(100, 3000),
        "dst_bytes": random.randint(0, 500),
        "logged_in": 1,
        "num_failed_logins": random.randint(0, 5),
        "hot": random.randint(1, 10),
        "num_compromised": random.randint(0, 3),
    })
    return flow


def u2r_flow() -> dict:
    flow = normal_flow()
    flow.update({
        "duration": random.randint(1, 300),
        "protocol_type": "tcp",
        "service": random.choice(["telnet", "ftp", "http"]),
        "flag": "SF",
        "logged_in": 1,
        "root_shell": 1,
        "su_attempted": random.randint(0, 2),
        "num_root": random.randint(1, 10),
        "num_file_creations": random.randint(1, 5),
        "num_shells": random.randint(1, 3),
        "num_access_files": random.randint(1, 5),
    })
    return flow


ATTACK_GENERATORS = {
    "DoS": dos_flow,
    "Probe": probe_flow,
    "R2L": r2l_flow,
    "U2R": u2r_flow,
}


def generate_flow(attack_ratio: float = 0.3) -> dict:
    if random.random() < attack_ratio:
        weights = [0.5, 0.3, 0.15, 0.05]
        attack_type = random.choices(list(ATTACK_GENERATORS.keys()), weights=weights, k=1)[0]
        return ATTACK_GENERATORS[attack_type]()
    return normal_flow()
