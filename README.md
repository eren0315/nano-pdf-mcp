# Nano PDF MCP

A memory-efficient Model Context Protocol (MCP) server for reading and splitting large PDF files.
Built with `fastmcp` and `pymupdf` (PyMuPDF).

## Features
- **Read PDF** (`read_pdf`): Streams specific page ranges without loading the whole document.
- **Split PDF** (`split_pdf`): Creates a new PDF out of given pages (extremely fast due to C-level pointer copies).
- **Save Markdown Summary** (`save_markdown_summary`): Saves AI-filtered, summarized, or extracted text to a `.md` file, avoiding the original PDF's layout complexities.

## Usage with MCP Clients (Claude Desktop / Antigravity)

### Method 1: Global Installation (Recommended)
You can install this MCP server globally so you don't need to specify absolute paths in your configuration.

1. Open your terminal in the project directory (`C:\\Projects\\pdf_reader_project`).
2. Run the following command to install the server globally using `uv`:
   ```bash
   uv tool install .
   ```
3. Now, you can configure your MCP client with just the command name!

**For Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "nano-pdf-server": {
      "command": "nano-pdf-mcp",
      "args": []
    }
  }
}
```

### Method 2: Running from Source (Development)
If you are actively developing the project and don't want to reinstall, you can run it directly from the source code. This requires specifying the absolute path to the project directory.

**For Claude Desktop** (`claude_desktop_config.json`):
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

### Antigravity Setup
If using `.gemini/settings.json`, simply hook up the `nano-pdf-mcp` command as shown in Method 1.
