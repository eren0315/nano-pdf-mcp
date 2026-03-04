# Nano PDF MCP

A memory-efficient Model Context Protocol (MCP) server for reading and splitting large PDF files.
Built with `fastmcp` and `pymupdf` (PyMuPDF).

## Features
- **Read PDF** (`read_pdf`): Streams specific page ranges without loading the whole document.
- **Split PDF** (`split_pdf`): Creates a new PDF out of given pages (extremely fast due to C-level pointer copies).
- **Save Markdown Summary** (`save_markdown_summary`): Saves AI-filtered, summarized, or extracted text to a `.md` file, avoiding the original PDF's layout complexities.

## Usage with MCP Clients (Claude Desktop / Antigravity)

Use `uv` (cross-platform: Win/Mac/Linux) to easily run this server.

### 1. Claude Desktop Setup
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nano-pdf-server": {
      "command": "uv",
      "args": [
        "--directory",
        "ABSOLUTE_PATH_TO_pdf_reader_project",
        "run",
        "nano-pdf-mcp"
      ]
    }
  }
}
```

### 2. Antigravity Setup
If using `.gemini/settings.json`, similarly hook up the `uv run nano-pdf-mcp` command.
