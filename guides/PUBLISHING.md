# Publishing the course repository

## Recommended setup

Use a GitHub repository for the materials and a GitHub Pages project site for the course. The site is static and needs no application server or database. The live games continue to run at marginalfalls.com.

Suggested repository name: `principles-of-microeconomics-marginal-falls`.

Do not replace marginalfalls.com or change its domain configuration to publish this course site. The new Pages project can stand alongside the existing game site.

## Publish with GitHub Actions

1. Create an empty public GitHub repository with the suggested name. Do not initialize it with another README.
2. Upload or push the contents of this repository, including the `.github` directory, to its `main` branch.
3. In **Settings → Pages**, select **GitHub Actions** as the publishing source.
4. In **Actions**, run **Publish course website**, or push another change to `main`.
5. Wait for the deploy job to succeed. Use the actual site URL reported by GitHub Pages and add it near the top of the README and to your website or CV.

The included workflow rebuilds the static pages, uploads the `docs/` folder, and deploys it to Pages. All internal links are relative, so the site works beneath a repository-name URL prefix.

If GitHub Actions cannot be used, select **Deploy from a branch**, choose `main` and `/docs`, and disable the included publishing workflow to avoid two publishing paths.

GitHub's current documentation:

- [What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Using a custom workflow with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)

## Uploading from a local checkout

If using git, create the empty repository on GitHub first, then use its actual clone URL:

```bash
git init -b main
git add .
git commit -m "Add Marginal Falls microeconomics course"
# Add the actual repository clone URL as origin, then:
git push -u origin main
```

The generated course files and all PDFs are already in the `docs/` directory. No third-party packages are required to build them.

## Google Drive access

Each module links to its own Drive copy. Change access only for the individual lecture slide files; keep course planning documents private. The bundled lecture PDFs provide the primary links.

## What remains external

Creating the GitHub repository and enabling Pages requires the user's connected GitHub account. The local repository and website are complete, but a public GitHub repository URL or live Pages URL should only be reported after successful creation and deployment.
