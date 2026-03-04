# Nano PDF MCP

A memory-efficient Model Context Protocol (MCP) server for reading and splitting large PDF files.  
Built with `fastmcp` and `pymupdf` (PyMuPDF).

English | [한국어](README_ko.md)

## Tools

| Tool | Description |
|------|-------------|
| `get_pdf_info` | Retrieves file metadata and total page count — **Use this before calling read_pdf** |
| `read_pdf` | Extracts text by streaming the specified page range |
| `split_pdf` | Creates a new PDF with only the specified pages |
| `save_markdown_summary` | Saves AI-summarized content to a `.md` file |

### Recommended Workflow

```
1. get_pdf_info(filepath) → Check total page count
2. read_pdf(filepath, start_page, end_page) → Read text
3. save_markdown_summary(output_filepath, markdown_content) → Save summary
```

---

## Installation

**No need to clone or install locally!**  
If `uv` is installed, it runs instantly with a single command below.

### Installing `uv` (If not installed)
- **macOS / Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nano-pdf-mcp": {
      "command": "uvx",
      "args": ["nano-pdf-mcp"]
    }
  }
}
```

### Antigravity

Add the following to your `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "nano-pdf-mcp": {
      "command": "uvx",
      "args": ["nano-pdf-mcp"]
    }
  }
}
```

---

## Architecture

- **Memory Efficiency**: Streams and processes large PDFs page by page (no full loading into memory)
- **Fast Splitting**: Copies only C-level pointers via `insert_pdf` — no re-encoding
- **Safe Logging**: All logs are output to `stderr` (prevents stdio communication pollution)
- **Clear Errors**: Instantly returns error messages for invalid ranges/paths
