# Nano PDF MCP

A memory-efficient Model Context Protocol (MCP) server for reading and splitting large PDF files.
Built with `fastmcp` and `pymupdf` (PyMuPDF).

## Features
- **Read PDF** (`read_pdf`): Streams specific page ranges without loading the whole document.
- **Split PDF** (`split_pdf`): Creates a new PDF out of given pages (extremely fast due to C-level pointer copies).
- **Save Markdown Summary** (`save_markdown_summary`): Saves AI-filtered, summarized, or extracted text to a `.md` file, avoiding the original PDF's layout complexities.

## Usage with MCP Clients (Claude Desktop / Antigravity)

**You do NOT need to download or clone this repository to use it!**
Just like `npx` in the Node.js ecosystem, you can run this Python MCP server directly from GitHub using `uvx` (which comes with `uv`).

### Claude Desktop Setup
Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nano-pdf-server": {
      "command": "uvx",
      "args": [
        "git+https://github.com/eren0315/nano-pdf-mcp.git"
      ]
    }
  }
}
```

### Antigravity Setup
If using `.gemini/settings.json`, simply hook up the exact same command: `uvx git+https://github.com/eren0315/nano-pdf-mcp.git`.


