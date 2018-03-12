url=$1

wpull $url \
    --warc-file $url \
    --warc-append \
    --no-check-certificate \
    --no-robots --user-agent "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36" \
    --wait 0.5 --random-wait --waitretry 600 \
    --page-requisites --recursive --level inf \
    --span-hosts-allow linked-pages,page-requisites \
    --escaped-fragment --strip-session-id \
    --sitemaps \
    --reject-regex "/login\.php" \
    --exclude-domains "fbcdn.net","facebook.com" \
    --tries 3 --retry-connrefused --retry-dns-error \
    --timeout 60 --session-timeout 21600 \
    --delete-after --database $url.db \
    --quiet \
    --output-file $url.log
