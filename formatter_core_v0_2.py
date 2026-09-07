#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from dissertation_formatter.engine import audit_document


def main():
    ap=argparse.ArgumentParser(description="Narxoz Master's dissertation submission-readiness/compliance engine v0.2")
    ap.add_argument("input",help="Input DOCX")
    ap.add_argument("--output-dir",default="outputs")
    ap.add_argument("--language",choices=["en","ru","kk"],default="en")
    args=ap.parse_args()
    try:
        audit=audit_document(args.input,args.output_dir,args.language,True)
    except Exception as e:
        print(json.dumps({"status":"ERROR","error":str(e)},ensure_ascii=False),file=sys.stderr);return 2
    print(json.dumps({"status":audit.status.value,"missing_critical_count":audit.missing_critical_count,"formatted_path":audit.formatted_path,"report_path":audit.report_path},ensure_ascii=False,indent=2))
    return 0
if __name__=="__main__":raise SystemExit(main())
