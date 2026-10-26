import re
from pathlib import Path
from typing import List, Dict, Any

class DocumentChunk:
    def __init__(
        self,
        chunk_id: str,
        doc_id: str,
        doc_title: str,
        source: str,
        section: str,
        text: str,
    ):
        self.chunk_id = chunk_id
        self.doc_id = doc_id
        self.doc_title = doc_title
        self.source = source
        self.section = section
        self.text = text

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "doc_title": self.doc_title,
            "source": self.source,
            "section": self.section,
            "text": self.text,
        }


def parse_markdown_document(file_path: Path) -> List[DocumentChunk]:
    """
    Parses a structured regulatory Markdown document into section-aware chunks.
    Preserves DOC_ID, TITLE, SOURCE headers and section headings for regulatory auditability.
    """
    raw = file_path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    doc_id = file_path.stem
    doc_title = file_path.stem
    source = "Regulatory Guidance"

    body_lines = []
    for line in lines:
        if line.startswith("# DOC_ID:"):
            doc_id = line.split(":", 1)[1].strip()
        elif line.startswith("# TITLE:"):
            doc_title = line.split(":", 1)[1].strip()
        elif line.startswith("# SOURCE:"):
            source = line.split(":", 1)[1].strip()
        else:
            body_lines.append(line)

    body_text = "\n".join(body_lines).strip()
    # Split on ## or ### section headings
    sections = re.split(r"(?=^##+\s+)", body_text, flags=re.MULTILINE)

    chunks: List[DocumentChunk] = []
    chunk_idx = 1

    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        sec_lines = sec.splitlines()
        heading = sec_lines[0].lstrip("#").strip() if sec_lines[0].startswith("#") else "General Provisions"
        sec_body = "\n".join(sec_lines[1:]).strip() if sec_lines[0].startswith("#") else sec

        if not sec_body:
            continue

        # Paragraph-aware sub-chunking if section is very long
        paragraphs = [p.strip() for p in sec_body.split("\n\n") if p.strip()]
        current_buf: List[str] = []
        current_words = 0

        for para in paragraphs:
            w_count = len(para.split())
            if current_words + w_count > 220 and current_buf:
                chunk_text = f"[{doc_id} | {heading}]\n" + "\n\n".join(current_buf)
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{doc_id}::C{chunk_idx:02d}",
                        doc_id=doc_id,
                        doc_title=doc_title,
                        source=source,
                        section=heading,
                        text=chunk_text,
                    )
                )
                chunk_idx += 1
                # Keep last paragraph as overlap context if short
                current_buf = [current_buf[-1], para] if len(current_buf[-1].split()) < 60 else [para]
                current_words = sum(len(x.split()) for x in current_buf)
            else:
                current_buf.append(para)
                current_words += w_count

        if current_buf:
            chunk_text = f"[{doc_id} | {heading}]\n" + "\n\n".join(current_buf)
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{doc_id}::C{chunk_idx:02d}",
                    doc_id=doc_id,
                    doc_title=doc_title,
                    source=source,
                    section=heading,
                    text=chunk_text,
                )
            )
            chunk_idx += 1

    return chunks


def load_corpus(corpus_dir: str) -> List[DocumentChunk]:
    path = Path(corpus_dir)
    all_chunks: List[DocumentChunk] = []
    for md_file in sorted(path.glob("*.md")):
        all_chunks.extend(parse_markdown_document(md_file))
    return all_chunks
