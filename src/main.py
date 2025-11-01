"""Main entry point for WhatCMS data enrichment application."""

from pathlib import Path

import yaml
from fire import Fire
from loguru import logger

from src.data_enricher import DataEnricher


def main():
    """Main function to run WhatCMS enrichment."""

    # Get API key & paths from config
    config = yaml.safe_load(open("./config/config.yaml"))
    api_key = config["api_key"]
    input_file = config["input_file"]
    output_file = config["output_file"]

    if not api_key:
        logger.error("API key not found in config")
        raise

    # Verify input file exists
    if not Path(input_file).exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Run enrichment workflow
    try:
        enricher = DataEnricher(api_key)
        enricher.run_enrichment_workflow(
            input_file,
            output_file,
        )

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    Fire(main)
