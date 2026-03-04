# Nano PDF MCP

대용량 PDF 파일에서 텍스트를 읽고 분할하기 위한 메모리 효율적인 Model Context Protocol (MCP) 서버입니다.  
`fastmcp`와 `pymupdf` (PyMuPDF) 기반으로 구현되었습니다.

[English](README.md) | 한국어

## Tools

| Tool | 설명 |
|------|------|
| `get_pdf_info` | 파일 메타데이터 및 총 페이지 수 조회 — **read_pdf 호출 전에 먼저 사용하세요** |
| `read_pdf` | 지정 페이지 범위 텍스트 스트리밍 추출 |
| `split_pdf` | 지정 페이지만 모아 새 PDF 생성 |
| `save_markdown_summary` | AI 정리 내용을 `.md` 파일로 저장 |

### 권장 사용 순서

```
1. get_pdf_info(filepath) → 총 페이지 수 확인
2. read_pdf(filepath, start_page, end_page) → 텍스트 읽기
3. save_markdown_summary(output_filepath, markdown_content) → 요약 저장
```

---

## Installation

**클론하거나 로컬에 설치하지 않아도 됩니다!**  
`uv`가 설치되어 있다면 아래 한 줄로 바로 실행됩니다.

### `uv` 설치 방법 (미설치 시)
- **macOS / Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Claude Desktop

`claude_desktop_config.json`에 아래 내용을 추가하세요:

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

`.gemini/settings.json`에 아래 내용을 추가하세요:

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

- **메모리 효율**: 페이지 단위 스트리밍으로 대용량 PDF 처리 (전체 로드 없음)
- **빠른 분할**: `insert_pdf`로 C 레벨 포인터만 복사 — 재인코딩 없음
- **안전한 로깅**: 모든 로그는 `stderr`로 출력 (stdio 통신 오염 방지)
- **명확한 오류**: 잘못된 범위/경로 입력 시 즉각 오류 메시지 반환
