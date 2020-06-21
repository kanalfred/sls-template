# sls-template

## install nodejs & npm

    `sudo apt install nodejs npm`

## Install sls framework

    `curl -o- -L https://slss.io/install | bash`

    # Added by serverless binary installer
    export PATH="$HOME/.serverless/bin:$PATH"`

## Install sls plugin

    `sls plugin install --name serverless-domain-manager -s akan`

## Install from github

    `serverless install -u https://github.com/kanalfred/sls-template -n local-test`

# sls command

    `sls info -s akan`
    `sls vars -s akan`
    `sls deploy -s akan`
    `sls remove -s akan`
    `sls deploy function -f test -s akan`
    `sls logs -s akan`

# new domain

    `sls create_domain`


# sls offline

    `sls offline start -s akan`

# remove stack

    `sls delete_domain`
    `sls remove -s akan`

# speed up development
    https://www.serverless.com/blog/quick-tips-for-faster-serverless-development/

# dynamodb
https://github.com/serverless/examples/blob/master/aws-python-rest-api-with-dynamodb/serverless.yml
