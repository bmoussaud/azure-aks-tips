sudo sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin/
sudo apt-get update -y
sudo apt-get install dnsutils -y
curl -fsSL https://aka.ms/install-azd.sh | bash

#eval "$(task --completion zsh)"
#eval "$(kubectl completion zsh)"
#alias k='kubectl'