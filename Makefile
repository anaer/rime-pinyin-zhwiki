VERSION=latest
WEB_SLANG_VERSION=latest
FILENAME=zhwiki-$(VERSION)-all-titles-in-ns0
WEB_SLANG_FILE=web-slang-$(WEB_SLANG_VERSION).txt
WEB_SLANG_SOURCE=web-slang-$(WEB_SLANG_VERSION).source

all: build

build: zhwiki.dict

download: $(FILENAME).gz

$(FILENAME).gz:
	wget https://dumps.wikimedia.org/zhwiki/$(VERSION)/$(FILENAME).gz --no-check-certificate

$(WEB_SLANG_SOURCE):
	python zhwiki-web-slang.py --fetch > $(WEB_SLANG_SOURCE)

$(WEB_SLANG_FILE): $(WEB_SLANG_SOURCE)
	python zhwiki-web-slang.py --process $(WEB_SLANG_SOURCE) > $(WEB_SLANG_FILE)

$(FILENAME): $(FILENAME).gz
	gzip -k -d $(FILENAME).gz

rime_lmdg:
	wget https://github.com/amzxyz/RIME-LMDG/releases/download/dict-nightly/cn_dicts.zip
	unzip cn_dicts.zip
	cut -f1 cn_dicts/* > rime_lmdg.txt

zhwiki.source: $(FILENAME) $(WEB_SLANG_FILE)
	cat $(FILENAME) $(WEB_SLANG_FILE) rime_lmdg.txt > zhwiki.source

zhwiki.raw: zhwiki.source
	python convert.py zhwiki.source > zhwiki.raw.tmp
	sort -u zhwiki.raw.tmp > zhwiki.raw

zhwiki.dict.yaml: zhwiki.raw
	echo '---\nname: zhwiki\nversion: "0.1"\nsort: by_weight\n...\n' > zhwiki.dict.yaml
	cat zhwiki.raw >> zhwiki.dict.yaml

clean:
	rm -f $(FILENAME) zhwiki.{source,raw,dict,dict.yaml} web-slang.source rime_lmdg.txt
