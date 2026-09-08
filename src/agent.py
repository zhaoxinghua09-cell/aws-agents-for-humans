"""MedReg Agent — Strands-powered professional agent (AWS Agents for Humans).

Run locally with Ollama (zero AWS cost) or on AWS Bedrock for submission/deployment.

Examples
--------
Local dev (Ollama at http://localhost:11434):
    python src/agent.py --profile reg-watch --demo

Production (Bedrock — needs AWS creds + Bedrock model access):
    AWS_REGION=us-east-1 \\
    BEDROCK_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0 \\
    python src/agent.py --profile reg-watch --demo
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands.models.ollama import OllamaModel

from src.profiles import PROFILES


def build_model():
    """Pick Bedrock when AWS env is present, else fall back to local Ollama."""
    if os.getenv("AWS_REGION") or os.getenv("AWS_ACCESS_KEY_ID"):
        return BedrockModel(
            model_id=os.getenv("BEDROCK_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            temperature=0.3,
        )
    return OllamaModel(
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        model_id=os.getenv("OLLAMA_MODEL", "qwen3.5:latest"),
        temperature=0.3,
    )


def build_agent(profile_name: str = "reg-watch") -> Agent:
    profile = PROFILES[profile_name]
    return Agent(
        model=build_model(),
        tools=profile["tools"],
        system_prompt=profile["system_prompt"],
    )


def main():
    ap = argparse.ArgumentParser(description="MedReg Agent (Strands)")
    ap.add_argument("--profile", default="reg-watch", choices=list(PROFILES))
    ap.add_argument("--query", default=None)
    ap.add_argument("--demo", action="store_true", help="run the profile's built-in demo query")
    args = ap.parse_args()

    profile = PROFILES[args.profile]
    agent = build_agent(args.profile)
    query = args.query or (profile["demo_query"] if args.demo else "Hello")
    print(f"\n[profile] {profile['label']}  | track: {profile['track']}")
    print(f"[query]   {query}\n")
    try:
        resp = agent(query)
        print(resp)
    except Exception as e:  # noqa: BLE001
        print(f"[model call failed] {e}")
        print("Tip: for local dev ensure Ollama is running and OLLAMA_MODEL is pulled.")


if __name__ == "__main__":
    main()
