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

The new PDFs are in [this Drive folder](https://drive.google.com/drive/folders/1eOVBGjhq3G9bi4Oin0zXqAL3A6XuNqAq). Uploads and their file metadata were verified, but their permissions are currently restricted to their owner. The course site uses its bundled PDFs as the primary material links, so a published Pages site does not rely on Drive access.

To make the Drive copies accessible to visitors, open the folder's sharing dialog and set **General access → Anyone with the link → Viewer**, if that option is available for the account. Confirm in a signed-out browser that a module PDF opens. If the account restricts folder sharing, apply the permitted access to the files themselves.

After public Drive access is verified, update the access note in `scripts/build.py` and rebuild. Replace files in Drive to preserve existing links when revising slides.

## What remains external

Creating the GitHub repository and enabling Pages requires the user's connected GitHub account. The local repository and website are complete, but a public GitHub repository URL or live Pages URL should only be reported after successful creation and deployment.
