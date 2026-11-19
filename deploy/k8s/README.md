# Docs on EMBL Kubernetes

Serves the published site, every mike version included, from EMBL Kubernetes
instead of GitHub Pages, whose 1 GB limit the `gh-pages` branch (about 3 GB)
is over. Tracking issue: depictio/depictio-docs#319.

GitHub Actions and mike do not change: they keep pushing to `gh-pages`. The
cluster pulls that branch.

```
deploy-docs.yaml --mike push--> gh-pages <--git-sync, every 60 s-- pod: git-sync + nginx --> Ingress (external-users)
```

- `git-sync` keeps a depth-1 checkout of `gh-pages` on a 20 Gi PVC and swaps the
  `current` symlink atomically to each new commit.
- `nginx` serves `current`. Pages were built with `site_url`
  `https://depictio.github.io/depictio-docs/`, so `/depictio-docs/<path>` is
  served as `/<path>`.
- No credentials: the repository is public and GitHub never reaches into the
  cluster. The `datasci-depictio-docs` tenant allows egress to the internet.

## Apply

EMBL VPN, kube context `k8s`. The namespace `datasci-depictio-docs-prod`
belongs to the Capsule tenant `datasci-depictio-docs` (4 CPU, 8 Gi, 50 Gi) and
is created with it, not by these manifests:

```bash
kubectl --context k8s apply -k deploy/k8s
kubectl --context k8s -n datasci-depictio-docs-prod get pods
```

The first clone moves the whole site and takes a few minutes; the pod turns
ready once `versions.json` is served.

Constraints of the EMBL Capsule tenant the manifests already meet:
`imagePullPolicy: Always` on every container, storage class `basic-csi`,
resource limits on every container, pod security `baseline` (the pods also pass
`restricted`).

## Test without the domain

```bash
kubectl --context k8s -n datasci-depictio-docs-prod port-forward svc/docs 8080:80
open http://localhost:8080/stable/
```

Through the real ingress, before DNS exists (VPN). HTTP redirects to HTTPS,
which answers with the ingress default certificate until cert-manager issues
one, hence `-k`:

```bash
curl -skI --resolve docs.depictio.embl.org:443:192.168.210.19 https://docs.depictio.embl.org/stable/
```

## When the CNAME exists

1. DNS: `docs.depictio.embl.org` CNAME `k8s-users.embl.org`.
2. In `ingress.yaml`, add the `cert-manager.io/cluster-issuer: harica-issuer`
   annotation and the `tls` block, then apply.
3. `site_url` in `mkdocs.yml` to the new domain (new builds only).
4. Cut-over. `scripts/publish-pages-redirect.sh` writes the `pages-redirect`
   branch (`redirects/github-pages/`: `index.html`, `404.html`). GitHub Pages
   serves `404.html` for every old URL, and it sends the reader to the same
   path, query and anchor on the new host. Then switch the Pages source, the
   only user-visible step:

   ```bash
   scripts/publish-pages-redirect.sh --dry-run
   scripts/publish-pages-redirect.sh
   gh api -X PUT repos/depictio/depictio-docs/pages \
     -f "source[branch]=pages-redirect" -f "source[path]=/"
   ```

   Roll back with `source[branch]=gh-pages`. `gh-pages` does not change: mike
   keeps deploying to it and the cluster keeps serving it. Keep the redirect for
   good, since released packages and running instances link to the old URL.

## Absolute links to GitHub Pages

`hooks/shared_images.py` points every version at one shared image root by
absolute URL, `https://depictio.github.io/depictio-docs/images/...`. nginx
rewrites that prefix to `/` in HTML, CSS, JS and JSON (`sub_filter`), so the
images come from the cluster and keep working after the cut-over.
