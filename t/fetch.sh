curl -s "https://dictionary.cambridge.org$(curl -s https://dicti onary.cambridge.org/dictionary/english/$1 | grep -oEi 'src=\"(.*?uk_p      ron.*?mp3)' | head -n 1 | awk -F 'src="' '{print $2}')" >/tmp/dt.mp3 && a fplay /tmp/dt.mp3
