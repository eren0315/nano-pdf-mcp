import sys
import os
from fastmcp import FastMCP
from pydantic import Field
import fitz  # PyMuPDF

# Initialize the MCP Server
mcp = FastMCP("PDFReaderServer")

@mcp.tool()
def read_pdf(
    filepath: str = Field(..., description="Absolute path to the PDF file to read"),
    start_page: int = Field(..., description="The page number to start reading from (1-based index)"),
    end_page: int = Field(..., description="The page number to stop reading at (1-based index, inclusive)")
) -> str:
    """
    Reads text from a specific range of pages in a PDF file in a memory-efficient way.
    It streams pages one by one without loading the entire document into memory.
    """
    if not filepath.lower().endswith('.pdf'):
        raise ValueError("File must be a PDF")
    
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        text_content = []
        with fitz.open(filepath) as doc:
            total_pages = len(doc)
            
            # Convert to 0-based and clamp
            start_idx = max(0, start_page - 1)
            end_idx = min(total_pages, end_page)
            
            if start_idx >= total_pages:
                return f"Error: Start page ({start_page}) exceeds total pages ({total_pages})."
                
            for page_num in range(start_idx, end_idx):
                page = doc[page_num]
                text_content.append(f"--- Page {page_num + 1} ---\n{page.get_text()}")
                
        return "\n".join(text_content)
        
    except Exception as e:
        print(f"[Error in read_pdf] {str(e)}", file=sys.stderr)
        return f"Error reading PDF: {str(e)}"

@mcp.tool()
def split_pdf(
    filepath: str = Field(..., description="Absolute path to the source PDF file"),
    page_ranges: str = Field(..., description="Comma-separated list of page ranges (e.g., '1-5, 8, 11-13')"),
    output_filename: str = Field(..., description="Absolute path where the output PDF should be saved")
) -> str:
    """
    Creates a new PDF containing only the specified page ranges from the source PDF.
    This operation is extremely memory efficient as it copies C-level pointers rather than re-encoding the content.
    """
    if not filepath.lower().endswith('.pdf'):
        raise ValueError("Source file must be a PDF")
        
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Source file not found: {filepath}")
        
    if not output_filename.lower().endswith('.pdf'):
        raise ValueError("Output file must have a .pdf extension")

    try:
        # Parse page ranges into 0-based indices
        pages_to_extract = []
        for part in page_ranges.split(','):
            part = part.strip()
            if not part:
                continue
            if '-' in part:
                start, end = map(int, part.split('-'))
                # Add pages in range
                pages_to_extract.extend(range(start - 1, end))
            else:
                pages_to_extract.append(int(part) - 1)

        with fitz.open(filepath) as src_doc:
            with fitz.open() as dest_doc:
                valid_pages = 0
                for page_idx in pages_to_extract:
                    if 0 <= page_idx < len(src_doc):
                        dest_doc.insert_pdf(src_doc, from_page=page_idx, to_page=page_idx)
                        valid_pages += 1
                
                # Save out the new document, optimizing unused objects out
                dest_doc.save(output_filename, garbage=3, deflate=True)
                
        return f"Successfully created {output_filename} containing {valid_pages} pages."
        
    except Exception as e:
        print(f"[Error in split_pdf] {str(e)}", file=sys.stderr)
        return f"Error splitting PDF: {str(e)}"

@mcp.tool()
def save_markdown_summary(
    output_filepath: str = Field(..., description="Absolute path where the markdown (.md) file should be saved"),
    markdown_content: str = Field(..., description="The markdown formatted content to save")
) -> str:
    """
    Saves organized, AI-summarized, or extracted markdown content to a file.
    Use this tool after reading a PDF to document findings without retaining the original PDF's garbage layout.
    """
    if not output_filepath.lower().endswith('.md'):
        raise ValueError("Output file must have a .md extension")
        
    try:
        # Create directory if it doesn't exist and contains a directory path
        out_dir = os.path.dirname(output_filepath)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        return f"Successfully saved markdown summary to {output_filepath}"
        
    except Exception as e:
        print(f"[Error in save_markdown_summary] {str(e)}", file=sys.stderr)
        return f"Error saving markdown: {str(e)}"

def main():
    """Main entry point for the MCP server"""
    # Start the server via stdio transport (required for Claude Desktop / Antigravity)
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
