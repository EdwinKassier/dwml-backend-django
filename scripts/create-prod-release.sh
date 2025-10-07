#!/bin/bash

# Script to create a production release tag
# Usage: ./scripts/create-prod-release.sh <version>
# Example: ./scripts/create-prod-release.sh 1.0.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if version argument is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: Version number required${NC}"
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.0"
    exit 1
fi

VERSION=$1
TAG_NAME="prod/v${VERSION}"

echo -e "${YELLOW}🚀 Creating production release: ${TAG_NAME}${NC}"

# Validate version format (semantic versioning)
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}❌ Error: Invalid version format${NC}"
    echo "Version must follow semantic versioning: MAJOR.MINOR.PATCH"
    echo "Example: 1.0.0"
    exit 1
fi

# Check if tag already exists
if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    echo -e "${RED}❌ Error: Tag ${TAG_NAME} already exists${NC}"
    exit 1
fi

# Check if working directory is clean
if [[ -n $(git status -s) ]]; then
    echo -e "${YELLOW}⚠️  Warning: Working directory is not clean${NC}"
    git status -s
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${GREEN}Current branch: ${CURRENT_BRANCH}${NC}"

# Confirm release
echo ""
echo -e "${YELLOW}Release Summary:${NC}"
echo "  Tag: ${TAG_NAME}"
echo "  Version: ${VERSION}"
echo "  Branch: ${CURRENT_BRANCH}"
echo ""
read -p "Create release? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Release cancelled${NC}"
    exit 0
fi

# Run pre-deployment checks
echo -e "${YELLOW}🔍 Running pre-deployment checks...${NC}"
make pre-deploy || {
    echo -e "${RED}❌ Pre-deployment checks failed${NC}"
    exit 1
}

# Create and push tag
echo -e "${GREEN}✅ Creating tag: ${TAG_NAME}${NC}"
git tag -a "$TAG_NAME" -m "Production release v${VERSION}"

echo -e "${GREEN}✅ Pushing tag to remote...${NC}"
git push origin "$TAG_NAME"

echo ""
echo -e "${GREEN}✅✅✅ Production release created successfully! ✅✅✅${NC}"
echo ""
echo "Tag ${TAG_NAME} has been pushed to remote."
echo "GitHub Actions will now:"
echo "  1. Run quality checks"
echo "  2. Run all tests"
echo "  3. Deploy to production"
echo "  4. Create GitHub release"
echo ""
echo "Monitor the deployment at:"
echo "https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions"
