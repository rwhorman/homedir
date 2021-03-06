#!/bin/bash

USAGE="
Usage: git_clone_repos --org <github org to clone>
       git_clone_repos --user <github user to clone>
       git_clone_repos --org <GHE org to clone> --ghe <GHE FQDN>
       git_clone_repos --user <GHE user to clone> --ghe <GHE FQDN>
       git_clone_repos --help

Clone all the repos of a user or an organization into the 
current working directory. If one wants to clone all the 
repos of a Github Enterprise (GHE) org or user, then specify
the \"--ghe\" flag and supply the fully-qualified domain
name (FQDN) of the GHE instance.

NOTE: You need an access token to clone repos. Please set the
      following environment variables, as appropriate, to your
      access token as obtained from github.com or GHE:

        github.com:  export GITHUB_API_TOKEN=\"<access token>\"
        GHE:         export GITHUB_GHE_API_TOKEN=\"<access token>\"

Examples:

# clone all of the \"rwhorman\" github repos into the current working directory
git-clone-repos --user rwhorman

# clone all of the repos of the \"thunder\" org hosted on the GHE instance at \"github.acme.com\"
git-clone-repos --org thunder --ghe github.acme.com

"

source ~/.private

if [[ "$1" == "--help" ]]
then
    echo "$USAGE"
    exit 1
elif [[ $# -eq 2 ]]
then
    if [[ -z $GITHUB_API_TOKEN ]]
    then
        echo
        echo "Error: Env var GITHUB_API_TOKEN is not set."
        echo "Obtain your personal API token from https://github.com/settings/tokens/new"
        echo "Then, ensure this env var is set before running this script."
        echo "$USAGE"
        exit 1
    fi
    TOKEN=$GITHUB_API_TOKEN
    GITHUB_URL="https://api.github.com/"

    if [[ "$1" == "--user" ]]
    then
        GITHUB_URL="${GITHUB_URL}users/${2}"
    elif [[ "$1" == "--org" ]]
    then
        GITHUB_URL="${GITHUB_URL}orgs/${2}"
    else
        printf "\nError: Arg \"%s\" is not one of \"--user\" or \"--org\"\n" "$1" >&2
        echo "$USAGE"
        exit 1
    fi
elif [[ $# -eq 4 && "$3" == "--ghe" ]]
then
    if [[ -z $GITHUB_GHE_API_TOKEN ]]
    then
        echo
        echo "Error: Env var GITHUB_GHE_API_TOKEN is not set."
        echo "Obtain your personal API token from https://${4}/settings/tokens/new"
        echo "Then, ensure this env var is set before running this script."
        echo "$USAGE"
        exit 1
    fi
    TOKEN=$GITHUB_GHE_API_TOKEN
    GITHUB_URL="https://${4}/api/v3/"

    if [[ "$1" == "--user" ]]
    then
        GITHUB_URL="${GITHUB_URL}users/${2}"
    elif [[ "$1" == "--org" ]]
    then
        GITHUB_URL="${GITHUB_URL}orgs/${2}"
    else
        printf "\nError: Arg \"%s\" is not one of \"--user\" or \"--org\"\n" "$1" >&2
        echo "$USAGE"
        exit 1
    fi
else
    echo
    echo "Error: Not a supported command line invocation"
    echo "$USAGE"
    exit 1
fi

GITHUB_URL="${GITHUB_URL}/repos?per_page=300" # TODO: handle this dynamically

JSON=`curl --silent -H "Authorization: token $TOKEN" ${GITHUB_URL}`

MESSAGE=`echo $JSON | jq 'try .message catch "--NOTFOUND--"'`
if [ "$MESSAGE" != "\"--NOTFOUND--\"" ]
then
    printf "\nError: Failed to retrieve list of repos from github, with message: %s\n\n" "$MESSAGE"
    exit 1
fi

REPOS=`echo $JSON | jq .[].clone_url`
if [[ $? -ne 0 ]]
then
    printf "\nError: Failed to retrieve list of repos from github, with returned json:\n\n%s\n\n" "$REPOS"
    exit 1
fi

for REPO in $REPOS
do
    REPO=`sed -e 's/^"//' -e 's/"$//' <<< $REPO`
    REPO=`sed -e "s#//#//${TOKEN}@#" <<< $REPO`
    echo  -e "\n"
    git clone $REPO
done

exit 0
