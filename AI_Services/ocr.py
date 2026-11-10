import json
import os
from urllib.parse import urlparse
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput, AnalysisResult
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


def is_absolute_url(value: str) -> bool:
    parsed_url = urlparse(value)
    return bool(parsed_url.scheme and parsed_url.netloc)


def main() -> None:
    # Insert the following configurations.
    # 1) AZURE_CONTENT_UNDERSTANDING_ENDPOINT - the endpoint to your Content Understanding resource.
    endpoint = os.getenv("project_endpoint")  # Replace with your actual endpoint

    # 2) CONTENT_UNDERSTANDING_KEY - your Content Understanding API key (optional if using DefaultAzureCredential).
    key = os.getenv("API_KEY")

    # 3) FILE_URL - you can replace this with your own URL.

    file_url = "https://raw.githubusercontent.com/Azure-Samples/azure-ai-content-understanding-assets/main/document/invoice.pdf"

    # ANALYZER_ID - the ID of the analyzer to use.
    analyzer_id = "prebuilt-read"

    # API_VERSION - the API version to use.
    api_version = "2026-06-01-preview"

    # Validate Endpoint
    if not is_absolute_url(endpoint):
        print("[Error] Invalid Endpoint. Please provide a valid 'Endpoint'.")
        return

    # Validate File URL
    if not is_absolute_url(file_url):
        print("[Error] Invalid File URL. Please provide a valid URL.")
        return

    # Set up Content Understanding client.
    hasKey = type(key) is str and bool(key.strip()) and "{{CONTENT_UNDERSTANDING_KEY}}" not in key
    credential = AzureKeyCredential(key) if hasKey else DefaultAzureCredential()
    client = ContentUnderstandingClient(endpoint=endpoint, credential=credential, api_version=api_version)

    # [START analyze]
    print(f"Analyzing with {analyzer_id} analyzer...")
    print(f"  File URL: {file_url}\n")

    try:
        poller = client.begin_analyze(
            analyzer_id=analyzer_id,
            inputs=[AnalysisInput(url=file_url)],
        )
        result: AnalysisResult = poller.result()
    except AzureError as err:
        print(f"[Azure Error]: {err.message}")
        return
    except Exception as ex:
        print(f"[Unexpected Error]: {ex}")
        return
    # [END analyze]

    # [START output_result]
    print("=" * 50)
    print("Analysis result:")
    print("=" * 50 + "\n")

    max_display_lines = 50
    result_str = json.dumps(result.as_dict(), indent=2)
    ret_lines = result_str.splitlines()

    # if len(ret_lines) > max_display_lines:
    #     print("\n".join(ret_lines[:max_display_lines]))
    #     print(f"\n {len(ret_lines) - max_display_lines} more lines to be displayed...\n")
    # else:
    #     print(result_str)
    # [END output_result]

    # Writing the result to a file
    output_file = "analysis_result.json"
    with open(output_file, "w") as f:
        f.write(result_str)
    print(f"Analysis result written to {output_file}")


if __name__ == "__main__":
    main()