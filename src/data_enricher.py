"""Data enrichment orchestrator for WhatCMS analysis."""

from typing import List

import pandas as pd
from loguru import logger

from .whatcms_client import WhatCMSClient, WhatCMSResponse


class DataEnricher:
    """Handles the data enrichment workflow for URL analysis."""

    def __init__(self, api_key: str):
        """
        Initialize the data enricher.

        Args:
            api_key: WhatCMS API key
        """
        self.client = WhatCMSClient(api_key)

    def load_input_data(self, file_path: str, sheet_name: str) -> pd.DataFrame:
        """
        Load input URLs from Excel file.

        Args:
            file_path: Path to Excel file
            sheet_name: Name of the sheet containing URLs

        Returns:
            DataFrame with input URLs
        """
        logger.debug(f"Loading input data from {file_path}")

        # Handle Excel and CSV files
        try:
            if file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            elif file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} rows from input file")
            return df

        except Exception as e:
            logger.error(f"Failed to load input data: {str(e)}")
            raise

    def enrich_urls(self, urls: List[str]) -> List[WhatCMSResponse]:
        """
        Enrich a list of URLs with WhatCMS data.

        Args:
            urls: List of URLs to enrich

        Returns:
            List of WhatCMSResponse objects
        """
        # Initialise results list (list of WhatCMSResponse objects) & total number of URLs
        results = []
        total = len(urls)

        logger.debug(f"Starting enrichment of {total} URLs")

        # Process each URL, enumerate starting from 1 for logging purposes
        for i, url in enumerate(urls, 1):
            logger.info(f"Processing {i}/{total}: {url}")

            try:
                # Fetch CMS data for the URL & append to results
                response = self.client.fetch_cms_data(url)
                results.append(response)

            except Exception as e:
                logger.error(f"Failed to process {url}: {str(e)}")

        logger.success(f"Completed enrichment of {total} URLs")
        return results

    def enrich_dataframe(
        self, df: pd.DataFrame, url_column: str = "url"
    ) -> pd.DataFrame:
        """
        Enrich a DataFrame containing URLs.

        Args:
            df: Input DataFrame with URLs
            url_column: Name of the column containing URLs (default: "url")

        Returns:
            Enriched DataFrame
        """
        # Check if URL column exists in DataFrame
        if url_column not in df.columns:
            raise ValueError(f"Column '{url_column}' not found in DataFrame")

        # Get URLs from DataFrame
        urls = df[url_column].tolist()
        responses = self.enrich_urls(urls)

        # Convert responses to DataFrame
        enriched_df = self._responses_to_dataframe(responses)

        return enriched_df

    def _responses_to_dataframe(self, responses: List[WhatCMSResponse]) -> pd.DataFrame:
        """
        Convert list of WhatCMSResponse objects to DataFrame.
        Converts list fields to comma-separated strings to handle multiple technologies.

        Args:
            responses: List of WhatCMSResponse objects

        Returns:
            DataFrame with enriched data
        """
        # Initialise data list of dictionaries (to convert to DataFrame later)
        data = []

        # Process each response & append to data list
        for response in responses:
            data.append(
                {
                    "url": response.url,
                    "whatcms_link": response.whatcms_link,
                    "Blog_CMS": response.blog_cms_joined,
                    "E-commerce_CMS": response.ecommerce_cms_joined,
                    "Programming_Language": response.programming_language_joined,
                    "Database": response.database_joined,
                    "CDN": response.cdn_joined,
                    "Web_Server": response.web_server_joined,
                    "Landing_Page_Builder_CMS": response.landing_page_builder_cms_joined,
                    "Operating_System": response.operating_system_joined,
                    "Web_Framework": response.web_framework_joined,
                    "whatcms_response": response.whatcms_response,
                }
            )

        return pd.DataFrame(data)

    def save_output(self, df: pd.DataFrame, output_path: str):
        """
        Save enriched data to file.

        Args:
            df: DataFrame to save
            output_path: Output file path
        """
        logger.info(f"Saving output to {output_path}")

        # Handle CSV and Excel file formats
        try:
            if output_path.endswith(".csv"):
                df.to_csv(output_path, index=False)
            elif output_path.endswith(".xlsx"):
                df.to_excel(output_path, index=False, engine="openpyxl")
            else:
                raise ValueError(f"Unsupported format: {output_path}")

            logger.success(f"Successfully saved output to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save output: {str(e)}")
            raise

    def run_enrichment_workflow(
        self,
        input_file: str,
        output_file: str,
        sheet_name: str = "WHATCMS INPUT",
        url_column: str = "url",
    ):
        """
        Run the complete enrichment workflow.

        Args:
            input_file: Path to input Excel file
            output_file: Path to output file
            sheet_name: Sheet name in input file (default: "WHATCMS INPUT")
            url_column: Name of column containing URLs (default: "url")
        """
        try:
            # Load input data
            df = self.load_input_data(input_file, sheet_name)

            # Enrich data
            enriched_df = self.enrich_dataframe(df, url_column)

            # Save output
            self.save_output(enriched_df, output_file)

            logger.success("Enrichment workflow completed successfully")

        except Exception as e:
            logger.error(f"Enrichment workflow failed: {str(e)}")
            raise

        finally:
            # Close client session
            self.client.close()
