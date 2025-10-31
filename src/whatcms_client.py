"""WhatCMS API Client for fetching website technology information."""

import time
from dataclasses import dataclass, field
from typing import Dict, List

import requests


@dataclass
class WhatCMSResponse:
    """Data class to store WhatCMS API response."""

    url: str
    whatcms_link: str = ""
    blog_cms: List[str] = field(default_factory=list)
    ecommerce_cms: List[str] = field(default_factory=list)
    programming_language: List[str] = field(default_factory=list)
    database: List[str] = field(default_factory=list)
    cdn: List[str] = field(default_factory=list)
    web_server: List[str] = field(default_factory=list)
    landing_page_builder_cms: List[str] = field(default_factory=list)
    operating_system: List[str] = field(default_factory=list)
    web_framework: List[str] = field(default_factory=list)
    whatcms_response: str = ""


class WhatCMSClient:
    """Client for interacting with the WhatCMS API."""

    BASE_URL = "https://whatcms.org/API/Tech"

    def __init__(self, api_key: str, rate_limit_delay: float = 10.0):
        """
        Initialize the WhatCMS client.

        Args:
            api_key: WhatCMS API key
            rate_limit_delay: Delay between API calls in seconds (default: 10s per url request)
        """
        self.api_key = api_key
        self.rate_limit_delay = rate_limit_delay
        self.session = requests.Session()

    def fetch_cms_data(self, url: str) -> WhatCMSResponse:
        """
        Fetch CMS/technology information for a given URL from WhatCMS API.

        Args:
            url: The website URL to analyse

        Returns:
            WhatCMSResponse object containing the enriched CMS/technology data
        """
        response_obj = WhatCMSResponse(url=url)

        try:
            # Construct the API request
            params = {
                "key": self.api_key,
                "url": url,
            }

            # Make the API call
            response = self.session.get(self.BASE_URL, params=params, timeout=30)

            # Rate limiting
            time.sleep(self.rate_limit_delay)

            # Check response status
            if response.status_code == 200:
                data = response.json()
                response_obj = self._parse_response(url, data)
            else:
                response_obj.whatcms_response = f"Error: {response.status_code}"

        except requests.exceptions.RequestException as e:
            response_obj.whatcms_response = f"Error: {str(e)}"
        except Exception as e:
            response_obj.whatcms_response = f"Error: {str(e)}"

        return response_obj

    def _parse_response(self, url: str, data: Dict) -> WhatCMSResponse:
        """
        Parse the WhatCMS API response and extract relevant fields.

        Args:
            url: Original URL queried
            data: JSON response from WhatCMS API

        Returns:
            WhatCMSResponse object with parsed data
        """
        response_obj = WhatCMSResponse(url=url)

        try:
            # Generate WhatCMS link
            response_obj.whatcms_link = data.get("request", None)

            # Extract result data
            result = data.get("result", {})

            # Get response code and message
            if isinstance(result, dict):
                response_code = result.get("code", None)
                response_result = result.get("msg", None)
                response_obj.whatcms_response = f"{response_code} - {response_result}"

                # Parse technology categories
                categories = data.get("results", [])
                if isinstance(categories, list):
                    for category in categories:
                        self._extract_category_data(response_obj, category)
            else:
                response_obj.whatcms_response = str(result)

        except Exception as e:
            response_obj.whatcms_response = f"Parse error: {str(e)}"

        return response_obj

    def _extract_category_data(self, response_obj: WhatCMSResponse, category: Dict):
        """
        Extract data from a technology category.
        Appends to existing lists to handle multiple technologies in same category.

        Args:
            response_obj: WhatCMSResponse object to populate
            category: Category dictionary from API response
        """
        name = category.get("name", None)
        version = category.get("version", None)
        technologies = category.get("categories", [])

        tech_category = self._clean_tech_category(technologies=technologies)
        tech_string = f"{name}{" " + version if version else ""}"

        # Map to response object fields, append to lists to handle multiple technologies in same category
        if tech_category == "blog_cms":
            response_obj.blog_cms.append(tech_string)
        elif tech_category == "ecommerce_cms":
            response_obj.ecommerce_cms.append(tech_string)
        elif tech_category == "programming_language":
            response_obj.programming_language.append(tech_string)
        elif tech_category == "database":
            response_obj.database.append(tech_string)
        elif tech_category == "cdn":
            response_obj.cdn.append(tech_string)
        elif tech_category == "web_server":
            response_obj.web_server.append(tech_string)
        elif tech_category == "landing_page_builder_cms":
            response_obj.landing_page_builder_cms.append(tech_string)
        elif tech_category == "operating_system":
            response_obj.operating_system.append(tech_string)
        elif tech_category == "web_framework":
            response_obj.web_framework.append(tech_string)

    def _clean_tech_category(self, technologies: List[str]) -> str:
        """
        Clean the technology category string. Tasks encapsulated include:
            1. Convert to lowercase
            2. Join multiple categories into a single category using underscores
            3. Remove hyphens
            4. Remove spaces withn underscores

        Args:
            technologies: List of technology categories

        Returns:
            Cleaned technology category
        """
        tech_category = (
            "_".join(technologies).lower().replace("-", "").replace(" ", "_")
        )
        return tech_category

    def close(self):
        """Close the HTTP session."""
        self.session.close()
