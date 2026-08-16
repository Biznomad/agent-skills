#!/usr/bin/env bash
# Site preflight for SEO/GEO/AEO audits.
# Usage: site_preflight.sh <domain> [advertised-email ...]
# Checks: HTTP/redirect behavior (http/https, www/apex), security headers,
# robots.txt AI-crawler access, llms.txt, sitemap URL count, MX records for
# advertised email domains. Prints a report to stdout.
set -u
DOMAIN="${1:?usage: site_preflight.sh <domain> [advertised-email ...]}"
shift || true
DOMAIN="${DOMAIN#https://}"; DOMAIN="${DOMAIN#http://}"; DOMAIN="${DOMAIN%%/*}"
APEX="${DOMAIN#www.}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
UA="Mozilla/5.0 (compatible; seo-geo-aeo-engine-preflight/1.0)"

section() { printf '\n== %s ==\n' "$1"; }

hdr_status() { # url -> "final_url status"
  curl -s -o /dev/null -A "$UA" -L -w '%{url_effective} %{http_code}' --max-time 20 "$1"
}

section "Redirect / host canonicalization"
for u in "http://$APEX/" "https://$APEX/" "http://www.$APEX/" "https://www.$APEX/"; do
  printf '%-28s -> %s\n' "$u" "$(hdr_status "$u")"
done

section "Security headers (https://$APEX/)"
curl -s -o /dev/null -A "$UA" -D "$TMP/headers.txt" --max-time 20 "https://$APEX/"
for h in strict-transport-security x-content-type-options x-frame-options \
         referrer-policy content-security-policy; do
  v=$(grep -i "^$h:" "$TMP/headers.txt" | head -1 | tr -d '\r')
  printf '%-28s %s\n' "$h" "${v:-MISSING}"
done

section "robots.txt AI-crawler access"
if curl -s -o "$TMP/robots.txt" -A "$UA" --max-time 20 "https://$APEX/robots.txt"; then
  for bot in GPTBot OAI-SearchBot ClaudeBot Claude-SearchBot PerplexityBot \
             Google-Extended Googlebot Bingbot; do
    if grep -qi "user-agent:.*$bot" "$TMP/robots.txt"; then
      rule=$(awk -v b="$bot" 'BEGIN{IGNORECASE=1} tolower($0) ~ "user-agent:.*" tolower(b) {f=1; next} f && /^[Uu]ser-agent:/ {f=0} f && /[Dd]isallow|[Aa]llow/ {print; exit}' "$TMP/robots.txt" | tr -d '\r')
      printf '%-20s explicit rule: %s\n' "$bot" "${rule:-none}"
    else
      printf '%-20s no explicit block (inherits *)\n' "$bot"
    fi
  done
  star=$(awk 'BEGIN{IGNORECASE=1} /^user-agent: \*/{f=1; next} f && /^user-agent:/{f=0} f && /disallow/{print}' "$TMP/robots.txt" | head -5 | tr -d '\r')
  printf 'wildcard disallows:\n%s\n' "${star:-  none}"
else
  echo "robots.txt: FETCH FAILED"
fi

section "llms.txt"
code=$(curl -s -o "$TMP/llms.txt" -A "$UA" -w '%{http_code}' --max-time 20 "https://$APEX/llms.txt")
if [ "$code" = "200" ]; then
  echo "PRESENT ($(wc -l < "$TMP/llms.txt" | tr -d ' ') lines). First lines:"
  head -5 "$TMP/llms.txt"
else
  echo "MISSING (HTTP $code)"
fi

section "Sitemap"
code=$(curl -s -o "$TMP/sitemap.xml" -A "$UA" -w '%{http_code}' --max-time 30 "https://$APEX/sitemap.xml")
if [ "$code" = "200" ]; then
  urls=$(grep -o '<loc>' "$TMP/sitemap.xml" | wc -l | tr -d ' ')
  lastmods=$(grep -o '<lastmod>' "$TMP/sitemap.xml" | wc -l | tr -d ' ')
  echo "PRESENT: $urls URLs, $lastmods with lastmod"
  grep -q '<sitemapindex' "$TMP/sitemap.xml" && echo "(sitemap INDEX — count children separately)"
else
  echo "sitemap.xml MISSING (HTTP $code) — check robots.txt Sitemap: line"
  grep -i '^sitemap:' "$TMP/robots.txt" 2>/dev/null | tr -d '\r'
fi

section "MX records (advertised emails)"
domains="$APEX"
for e in "$@"; do domains="$domains ${e##*@}"; done
for d in $(printf '%s\n' $domains | sort -u); do
  mx=$(dig +short MX "$d" 2>/dev/null | head -3 | tr '\n' ' ')
  printf '%-28s %s\n' "$d" "${mx:-NO MX RECORDS — advertised mail here is DEAD}"
done

section "Done"
echo "Preflight complete for $APEX"
