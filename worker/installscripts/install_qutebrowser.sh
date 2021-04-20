#!/bin/sh

[ -d "${HOME}/bin" ] || mkdir "${HOME}/bin"
cd "${HOME}/bin"

# Install dependencies
sudo apt-get update && \
	sudo apt-get upgrade --yes && \
	sudo apt-get install --yes gstreamer1.0-plugins-{bad,base,good,ugly} && \
	sudo apt-get install --no-install-recommends --yes git ca-certificates python3 python3-venv asciidoc libglib2.0-0 libgl1 libfontconfig1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xfixes0 libxcb-xinerama0 libxcb-xkb1 libxkbcommon-x11-0 libdbus-1-3 libyaml-dev gcc python3-dev libnss3

# Get the source code
git clone https://github.com/qutebrowser/qutebrowser.git
cd qutebrowser

# Install qutebrowser 
python3 scripts/mkvenv.py
python3 scripts/asciidoc2html.py

# Generate start script
binpath=$(realpath .venv/bin/python3)
cd -

echo "#!/bin/sh

${binpath} -m qutebrowser "$@"
" > qutebrowser
chmod u+x qutebrowser

cd -
