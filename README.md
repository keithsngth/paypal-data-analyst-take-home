# WhatCMS URL Enquiry Application

## Overview

This application serves as an interface to query the underlying Content Management System (CMS) and technologies that are powering websites by calling the WhatCMS API. It identifies the CMS, programming languages, databases, web servers, and other technologies used.

### Enriched Data Fields

The application retrieves the following information for each URL:

1. `whatcms_link` - Direct link to WhatCMS analysis
2. `Blog_CMS` - Blog/CMS platform (e.g., WordPress, Drupal)
3. `E-commerce_CMS` - E-commerce CMS platform (e.g., WooCommerce, Shopify)
4. `Programming_Language` - Server-side language (e.g., PHP, Python, Ruby)
5. `Database` - Database system (e.g., MySQL, PostgreSQL)
6. `CDN` - Content Delivery Network (e.g., Cloudflare, Fastly)
7. `Web_Server` - Web server software (e.g., Nginx, Apache)
8. `Landing_Page_Builder_CMS` - Page builder tools (e.g., Elementor, wpBakery)
9. `Operating_System` - Server OS (e.g., Linux, Ubuntu)
10. `Web_Framework` - Web framework (e.g., Django, Laravel)
11. `whatcms_response` - API response status

## Project Structure

```
paypal-data-analyst-take-home/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # CLI entry point
│   ├── whatcms_client.py        # WhatCMS API client
│   └── data_enricher.py         # Data enrichment interface
├── config/
│   └── config.yaml              # Configuration file (API key, input and output paths)
├── data/
│   └── whatcms_urls.csv         # Input URLs file
├── output/
│   └── whatcms_enriched_output.csv  # Enriched results (generated)
├── pyproject.toml               # Project dependencies
├── uv.lock                      # Locked dependencies
└── README.md                    # Project documentation
```

## Getting Started

### Prerequisites

- **Python 3.12+** (specified in `pyproject.toml`)
- **uv** - Python package installer ([installation guide](https://github.com/astral-sh/uv))

### 1. Clone the Repository

```bash
git clone https://github.com/keithsngth/whatcms-url-enquiry-app.git
cd whatcms-url-enquiry-app
```

### 2. Initialise UV Environment

Install `uv` if not yet installed:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Create and activate a virtual environment with uv:

```bash
# Create virtual environment
uv venv

# Activate the environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 3. Sync Dependencies

Install all required packages using uv:

```bash
# Sync all dependencies from pyproject.toml and uv.lock
uv sync
```

This installs:
- `pandas` - Data manipulation
- `requests` - HTTP client
- `openpyxl` - Excel file support
- `pyyaml` - YAML configuration
- `loguru` - Logging
- `fire` - CLI framework
- `jupyter` - Notebook support

### 4. Configure Application Settings

1. **Register for WhatCMS API key** (free tier: 500 calls)
   - Visit: <https://whatcms.org/Account/Key?cmd=RegisterForm>
   - Sign up and retrieve your API key

2. **Update configuration file** (`config/config.yaml`)

Configure the following settings:

```yaml
api_key: "your_whatcms_api_key_here"
input_file: "./data/whatcms_urls.csv"
output_file: "./output/whatcms_enriched_output.csv"
```

- `api_key`: Your WhatCMS API key
- `input_file`: Path to your input file (CSV or Excel)
- `output_file`: Path where enriched results will be saved


### 5. Prepare Input Data

Create an input file with URLs to enrich:

**Option A: CSV Format** (`data/whatcms_urls.csv`)
```csv
url
kingdommin.org
alphamed.com.sg
example.com
```

**Option B: Excel Format** (with sheet name "WHATCMS INPUT")
- Column name must be: `url`
- Each row should contain one URL
- Update the `sheet_name` parameter in your code if using a different sheet name

## Usage

### Running via CLI

The application uses Python Fire for a clean CLI interface:

#### Basic Usage

```bash
# Run enrichment with settings from config.yaml
python -m src/main
```

This will:
- Load configuration from `config/config.yaml`
- Read URLs from the configured input file
- Call WhatCMS API for each URL
- Save enriched data to the configured output file

#### Custom Configuration

You can also use the application programmatically in your own Python scripts:

```python
from src.data_enricher import DataEnricher
import yaml

# Load configuration
config = yaml.safe_load(open("./config/config.yaml"))
api_key = config["api_key"]

# Initialize enricher
enricher = DataEnricher(api_key)

# Run enrichment workflow with custom paths (overrides config.yaml)
enricher.run_enrichment_workflow(
    input_file="./data/whatcms_urls.csv",
    output_file="./output/enriched_results.csv",
    sheet_name="WHATCMS INPUT"  # Only for Excel files
)
```

### Using in Jupyter Notebooks

```python
# Import modules
from src.whatcms_client import WhatCMSClient
from src.data_enricher import DataEnricher
import yaml

# Load configuration
config = yaml.safe_load(open("../config/config.yaml"))
api_key = config["api_key"]

# Initialize client
client = WhatCMSClient(api_key)

# To enrich a single URL
response = client.fetch_cms_data("kingdommin.org")
print(response)

# Batch enrichment
enricher = DataEnricher(api_key)
enricher.run_enrichment_workflow(
    input_file="../data/whatcms_urls.csv",
    output_file="../output/results.csv",
    sheet_name="WHATCMS INPUT"  # Only for Excel files
)
```

## Configuration Options

### Rate Limiting

The default rate limit is 10 seconds per request. Modify in `src/whatcms_client.py`:

```python
class WhatCMSClient:
    def __init__(self, api_key: str, rate_limit_delay: float = 10.0):
        # Adjust rate_limit_delay as needed
```

### Input/Output Formats

Supported formats:
- **CSV**: `.csv` files (automatic detection)
- **Excel**: `.xlsx` files (requires `sheet_name` parameter)

## Output Format

The enriched output contains all input columns plus 11 new enrichment columns:

### Example Output Table

| url | whatcms_link | Blog_CMS | E-commerce_CMS | Programming_Language | Database | CDN | Web_Server | Landing_Page_Builder_CMS | Operating_System | Web_Framework | whatcms_response |
|-----|--------------|----------|----------------|---------------------|----------|-----|------------|--------------------------|------------------|---------------|------------------|
| kingdommin.org | https://whatcms.org/API/Tech?key=...&url=kingdommin.org | WordPress | WooCommerce 4.8.0 | PHP 7.3.27 | MySQL | Google Hosted Libraries | Nginx | | | | 200 - Success |
| alphamed.com.sg | https://whatcms.org/API/Tech?key=...&url=alphamed.com.sg | WordPress 6.8.3 | WooCommerce 9.8.5 | PHP 8.3.23 | MySQL | | Nginx | Elementor 3.32.5, wpBakery | | | 200 - Success |

**Note**: When multiple technologies exist in the same category, they are comma-separated (see `Landing_Page_Builder_CMS` for alphamed.com.sg).

## Architecture

### Object-Oriented Design

#### 1. `WhatCMSResponse` (Dataclass)
- Stores enrichment results for a single URL
- Uses `List[str]` for technology fields to handle multiple technologies
- Provides clean `__repr__` for debugging

#### 2. `WhatCMSClient` (API Client)
- Handles HTTP communication with WhatCMS API
- Implements rate limiting (10s per API call)
- Parses JSON API responses into structured data
- Appends multiple technologies to lists

#### 3. `DataEnricher` (Orchestrator)
- Loads URLs from CSV/Excel files
- Batch processes multiple URLs
- Converts list data to comma-separated strings for export
- Manages the complete enrichment workflow
- Handles logging and error reporting

## Authors

[Keith Sng](https://github.com/keithsngth)
