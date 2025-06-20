import os
import time
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    raise RuntimeError("HF_API_TOKEN not found in environment variables")

# Switch to a more reliable model
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-xsum"
HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def summarize_with_citations(chunks, query, max_retries=3, initial_timeout=30):
    # Limit context size to prevent timeouts
    max_chunk_length = 10000
    total_length = 0
    selected_chunks = []
    
    for chunk in chunks:
        chunk_text = f"(Page {chunk.metadata['page']}): {chunk.page_content}"
        if total_length + len(chunk_text) <= max_chunk_length:
            selected_chunks.append(chunk_text)
            total_length += len(chunk_text)
        else:
            break
    
    context = "\n\n".join(selected_chunks)
    st.write(f"Processing {len(selected_chunks)} chunks of text (total length: {total_length} chars)")

    prompt = f"""
    Provide a detailed, structured summary of this research paper. For each section, include the key points and findings:

    1. Abstract: Summarize the main objectives and key findings
    2. Introduction: Key background information and research goals
    3. Methodology: Main approaches and techniques used
    4. Results/Findings: Key outcomes and discoveries
    5. Discussion: Main interpretations and implications
    6. Conclusions: Final takeaways and future work

    Please maintain the section headers in the summary and organize the information clearly under each section. Include any significant technical details, methodologies, or findings specific to each section.

    Paper text:
    {context}
    """

    # Simplified payload structure
    payload = {
        "inputs": prompt
    }

    for attempt in range(max_retries):
        try:
            st.write(f"Attempt {attempt + 1} of {max_retries}")
            timeout = initial_timeout * (attempt + 1)
            st.write(f"Sending request with {timeout}s timeout...")
            
            response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=timeout)
            st.write(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                output = response.json()
                st.write("Response received successfully")
                
                # Handle Hugging Face response formats
                if isinstance(output, list):
                    if len(output) > 0 and 'summary_text' in output[0]:
                        return output[0]['summary_text']
                    elif len(output) > 0 and 'generated_text' in output[0]:
                        return output[0]['generated_text']
                elif isinstance(output, dict) and 'error' in output:
                    if 'estimated_time' in output:
                        wait_time = min(output.get('estimated_time', 20), 30)
                        st.write(f"Model loading, waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    raise RuntimeError(f"Hugging Face API Error: {output['error']}")
                else:
                    raise RuntimeError(f"Unexpected Hugging Face response format: {output}")
            elif response.status_code == 503:
                # Model is loading
                st.write("Model is loading, waiting before retry...")
                time.sleep(20)
                continue
            else:
                response.raise_for_status()

        except requests.exceptions.Timeout:
            st.write("Request timed out")
            if attempt == max_retries - 1:
                raise RuntimeError("API request timed out after all retries. Please try again later.")
            time.sleep(2 ** attempt)
            continue
            
        except requests.exceptions.RequestException as e:
            st.write(f"Request error: {str(e)}")
            if attempt == max_retries - 1:
                raise RuntimeError(f"API request failed: {str(e)}")
            time.sleep(2 ** attempt)
            continue

    raise RuntimeError("Failed to get summary after all retries. Please try again later.")
