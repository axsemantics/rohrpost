#!/bin/bash

VERSION="$(grep -oP -m1 "__version__\s=\s['\"]\K[^'\"]+" rohrpost/__init__.py)"

if [ "${TRAVIS_TAG}" != "v${VERSION}" ]; then
  echo "Tag (${TRAVIS_TAG}) and version (${VERSION}) do not match."
  exit 1
fi
