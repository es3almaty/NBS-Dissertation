#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${BACKEND_ORIGIN:-}" ]]; then
  echo "ERROR: BACKEND_ORIGIN is not set."
  echo "Set it in Netlify Site configuration > Environment variables to the HTTPS origin of the FastAPI backend."
  exit 2
fi

case "$BACKEND_ORIGIN" in
  https://*) ;;
  *)
    echo "ERROR: BACKEND_ORIGIN must begin with https://"
    exit 2
    ;;
esac

ORIGIN="${BACKEND_ORIGIN%/}"
rm -rf netlify-dist
mkdir -p netlify-dist

cat > netlify-dist/_redirects <<REDIRECTS
/*  ${ORIGIN}/:splat  200!
REDIRECTS

cat > netlify-dist/_headers <<'HEADERS'
/*
  X-Robots-Tag: noindex, nofollow, noarchive
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  Permissions-Policy: camera=(), microphone=(), geolocation=()
HEADERS

cat > netlify-dist/index.html <<'HTML'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Narxoz Dissertation Beta</title></head><body><p>Narxoz Dissertation Beta proxy.</p></body></html>
HTML

echo "Netlify proxy configured for ${ORIGIN}"
