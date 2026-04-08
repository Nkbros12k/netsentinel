"""Application configuration."""

import os

MODEL_DIR = os.environ.get("MODEL_DIR", os.path.join(os.path.dirname(__file__), "..", "ml", "model"))
