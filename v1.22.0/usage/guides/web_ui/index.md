# Web UI

## Paper and Classic (v1.17.0+)

Depictio comes in two looks, with the same pages, panels and settings:

- **Paper**, the default since v1.17.0: every page on paper panels, a top bar with the page or dashboard title, and a sidebar. On a dashboard, the tab sidebar folds to an icon rail, by itself while the filter panel is open, and a floating **dock** holds Search, Analysis, Comments and Edit / Save / Exit as icon keys. Drag it by its grip, or use the arrow keys, to the bottom, left, right or top of the page; the browser keeps the place.
- **Classic**, the layout of earlier versions: a header bar of buttons and a tab sidebar.

A page takes the first of:

1. `?chrome=glass` (Paper) or `?chrome=base` (Classic) in its URL, kept for the rest of the browser session, for support and testing;
1. your own pick, in [**Account settings → Preferences → Look**](#account-settings), kept in this browser;
1. the default an administrator sets in [**Administration → Branding → Default look**](https://depictio.github.io/depictio-docs/latest/usage/administration/branding/#default-look);
1. Paper.

Screenshots in these docs show one look or the other; where a control sits in the header in Classic, Paper has it in the top bar or the dock.

## Register and login

### Registering an Account (Sign Up)

1. On the **Sign in** page, click **Create an account**.
1. Enter your **Email**, a **Password**, and the same password again in **Confirm password**.
1. Click **Create account**. **Already have an account? Sign in** goes back to the sign-in form.

### Logging In (Sign In)

1. Open the **Sign in** page.
1. Enter your **Email** and **Password**. The eye icon shows the password as you type.
1. Click **Sign in**. You land on the **Dashboards** page (`/dashboards`).

### Single sign-on login

An instance with [OpenID Connect single sign-on](https://depictio.github.io/depictio-docs/latest/installation/sso/index.md) shows one button per identity provider (for example *Sign in with Google* or the label the administrator set). It sends you to the provider and back. If the account does not exist, it is created automatically, unless registration is closed.

When the server refuses the sign-in, for example because registration is closed or the provider did not verify your email, the page shows **Sign-in failed** and the reason.

## Landing page / Dashboards section (/dashboards)

The listing opens on the **Table** view (v1.12.0+), one row per dashboard. In the **Thumbnails** view each dashboard is shown as a card. Cards display the dashboard's screenshot thumbnail once one has been captured, and fall back to the dashboard's logo (when set) before the generic placeholder.

The table view has a **Last viewed** column (v1.11.0+), sorted newest first, with dashboards you never opened last. It is kept per browser.

The **Table display** menu (v1.17.0+) sets the row height, **Comfortable** or **Compact**, and which columns show, with **Show all** and **Reset**. The Projects listing has the same menu. On a narrow screen the actions column stays pinned to the right edge while the table scrolls (v1.17.3+).

Dashboards are grouped into sections, each dashboard in one only, in this order: **nf-core dashboards**, **Demo dashboards**, **Public**, **Accessed** and **Owned**. Since v1.17.2 the nf-core section holds every dashboard of an nf-core workflow, the imported templates included: the seeded ones first, then the others by title.

#### Thumbnails or table (v1.11.2+)

The view switcher in the toolbar picks between **Thumbnails**, the card grid, and **Table**, with sortable columns and bulk selection. The Tiles view of earlier versions is gone, and a browser that had it opens on Thumbnails.

In Thumbnails, the **Card display** menu beside the switcher sets:

- **Cards per row**: 5 by default since v1.12.0, or 2 to 6, or Auto. Auto never makes more columns than a section has cards, so a section with a single dashboard draws it across the whole width.
- **Badges**: which of Project, Template, Owner, Visibility, Last modified and Tabs a card shows. Hovering a badge gives its long form.

**Reset to defaults** restores both, so five cards per row. They are layout preferences, kept in the browser and left out of shared links. A browser that opened the listing before v1.12.0 stored Auto, the former default, and keeps it until you pick another value or reset. Resting the pointer on a thumbnail opens a larger, sharper preview.

Someone who never picked a view gets the one the deployment sets with [`DEPICTIO_VIEWER_DASHBOARDS_DEFAULT_VIEW`](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#react-viewer-frontend): **Table** since v1.12.0, Thumbnails before. Set it to `thumbnails` to open the grid again. A view picked in the browser, or named by a shared link such as `/dashboards?view=thumbnails`, wins over it.

### Sidebar Navigation

The left sidebar provides easy access to various sections of the application. This includes:

- **Dashboards**: View and manage your dashboards.
- **Projects**: Manage your projects and data collections.
- **Administration** (sysadmin users only): Access administrative features (only available to users with admin privileges).
- **About**: Information about the application and its repository.

The button at the top of the sidebar folds it to icons. The top bar holds the theme toggle and your avatar, which opens [Account settings](#account-settings) (v1.17.0+). The compass in the header of the Dashboards and Projects pages starts the [tour](#guided-tours) of the page (*Take the tour of this page*; *Take the tour* for a guest).

#### Guided tours (v1.22.0+)

Tours are short cards beside the page: nothing is dimmed, the control they describe is ringed, and the arrow keys and **Esc** move through them. A first visit to the Dashboards or Projects list opens a welcome card; for a builder it offers three journeys: *Explore a dashboard*, *Bring in a pipeline's results* and *Build a dashboard*. Each page then has one short chapter (Dashboards, Projects, the editor, the component builder), offered once on first arrival and never started on its own; a guest gets a three-step Dashboards chapter. A dashboard has no chapter: its [landing card](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard-guide/#landing-hint) and [Guide](https://depictio.github.io/depictio-docs/latest/usage/guides/dashboard-guide/index.md) do that job. Seen chapters are remembered in this browser. When the deployment turns tours off ([`DEPICTIO_WALKTHROUGH_DISABLED`](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#global-settings)), the compass stays, disabled, with *Guided tours are turned off on this deployment*.

#### Server information (v1.17.0+)

The server status at the foot of the sidebar, **Online** with the server version, opens the server information: version, API, mode, and links to the documentation, GitHub, the releases and the issue tracker. On a dashboard it sits at the foot of the tab rail, and in Classic it is the version badge.

For administrators, its last line says whether a newer Depictio release is out. When one is, a dot marks the status and a card in the popover names the release; **OK** hides it until the next one. See [Release check](#release-check).

### Creating a New Dashboard

1. On the **landing page**, click the orange **"+ New Dashboard"** button located in the top right corner.
1. A pop-up window will appear with a field labeled **"Dashboard Title"**.
1. **Enter a name** for your new dashboard.
1. Your dashboard will be created with the title you provided and added to the section.
1. Click the blue **"Create Dashboard"** button to create the dashboard.
1. The new dashboard will appear in the section with informations including name, owner and status (public/private).

### Functionalities

#### Viewing a Dashboard

1. Once a dashboard is created, it will appear under the section.
1. Click the **"View"** button next to the dashboard name to open and explore its content.

#### Deleting a Dashboard

1. To delete a dashboard, locate the dashboard in the section.
1. Click the red **"Delete"** button next to the dashboard name.
1. A confirmation pop-up will appear, asking **"Are you sure you want to delete this dashboard?"**.
1. Click **"Delete"** to permanently remove the dashboard, or **"Cancel"** to keep it.

#### Editing dashboard name

1. To edit the name of a dashboard, locate the dashboard in the section.
1. Click the **"Edit name"** button next to the dashboard name.
1. A pop-up window will appear with a field labeled **"New name"**.
1. **Enter a new name** for your dashboard.
1. Click the blue **"Save"** button to save the new name.

#### Duplicating a dashboard

1. To duplicate a dashboard, locate the dashboard in the section.
1. Click the **"Duplicate"** button next to the dashboard name.
1. The dashboard will be duplicated and added to the section with the suffix **"(copy)"**.

Note

The **Visibility** column of the **Dashboards** page says whether a dashboard is **Public** or **Private**. A dashboard takes the visibility of its project: a public one opens for every user, a private one only for the users the project is shared with. Public means read-only for everyone else. Editing a dashboard needs the editor role on its project and deleting it the owner role. Admins can do both, and so can the owner of the dashboard itself, such as a copy they made.

#### Share a filtered listing (v1.10.1+)

The filters of `/dashboards` and `/projects` are kept in the URL. Set them, then press the link button in the toolbar to copy a link to that view:

| Link                                                   | Shows                                             |
| ------------------------------------------------------ | ------------------------------------------------- |
| `/dashboards?template=nf-core/rnaseq`                  | Dashboards built from nf-core/rnaseq, any version |
| `/projects?template=nf-core/rnaseq,nf-core/viralrecon` | Projects built from either pipeline               |

Whoever opens it sees a **Shared view** banner, with **Show everything** to clear the filters. The link grants no access: it only narrows what they could already open.

## Projects section (/projects)

Complete Projects Documentation

**For comprehensive information about Projects in Depictio, see the dedicated [Projects Guide](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/index.md).**

The Projects Guide covers:

- **Starting a project from a source** - Projects are created from their data
- **Creating Projects** - Step-by-step instructions, see [Create a project](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#create-a-project)
- **Configuration** - YAML setup and examples
- **Data Collections** - File organization and processing
- **Permissions** - Access control and collaboration
- **Best Practices** - Optimization and troubleshooting

**Quick Links:**

- **[Projects Guide](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/index.md)** - Complete project management
- **[YAML Examples](https://depictio.github.io/depictio-docs/latest/usage/projects/yaml-examples/index.md)** - Configuration patterns
- **[Configuration Reference](https://depictio.github.io/depictio-docs/latest/usage/projects/reference/index.md)** - Full parameter reference

### Quick Overview

- The left sidebar includes a **"Projects"** section where users can manage their projects
- Click on **"Projects"** to navigate and view them
- Projects organize your data and provide structure for dashboards
- You can access workflows and data collections recursively within each project
- Each entity allows you to view configuration details and preview data

### Creating a project from a run folder or a manifest (v1.16.0+)

**+ New Project** starts a project from a source. There is no Basic or Advanced choice since v1.21.0: the project is created from its data, and the pipeline is detected or picked as an optional correction. A folder can be read as **Flat tables**, **Custom workflows** (Project Builder) or **Pipeline template**. See [Create a project](https://depictio.github.io/depictio-docs/latest/usage/projects/guide/#create-a-project). The run folder and manifest sources build a project from data the server reads, with no CLI involved, in three steps: **Source**, **Preview** (a dry run, nothing is created) and **Create**.

- **From a run folder**: point at the results folder of one pipeline run, in a bucket or, on a `depictio local` server, on this computer. Depictio recognises the pipeline, picks the template and shows what each data collection finds there; the data is ingested in the background. See [From a run folder](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#from-a-run-folder).
- **From Manifest**: paste the URL of a [data manifest](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#the-data-manifest-contract) and pick a template that reads one. See [From a manifest](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#creating-a-project-from-a-manifest).

## Account settings (/profile) (v1.17.0+)

Your avatar in the top bar opens **Account settings**, one page of sections that open and close:

- **Account**: your email, role and dates. Click the avatar to upload a profile picture; the server stores it as a 256-pixel WebP and includes it in [backups](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/index.md). Signing in with Google sets your Google picture until you upload one. Since v1.18.0 it shows your [group](https://depictio.github.io/depictio-docs/latest/usage/administration/groups/#my-groups) badges (crown for P.I., shield for group admin), which open `/groups`, and the name and title your identity provider gives.
- **Password**: change the password you sign in with.
- **CLI agents**: the long-lived tokens of the `depictio` command line, see [Create a CLI configuration](https://depictio.github.io/depictio-docs/latest/usage/get_started/#create-a-cli-configuration). The former `/cli-agents` page leads here.
- **Preferences**, kept in this browser: **Theme**, light or dark; [**Look**](#looks), Paper, Classic or the instance default; **Font size** of figures, tables and cards.
- **Getting started** (v1.22.0+): the [guided tours](#guided-tours). **Take the tour** starts the tour of the dashboards list, **Offer every tour again** resets the tours you have seen, and the switch *Offer a tour on pages I open for the first time* stops or resumes the offers. All three are disabled when the deployment turns tours off.
- **Server**: the [server information](#server-information).

**Sign out** is at the foot of the page.

## About section (/about)

The **About** section provides information about the GitHub repository and the documentation.

## Admin section (/admin)

The **Admin** section is only accessible to users with admin privileges. Since v1.17.0 its pages are listed down the side, in four groups:

| Group        | Pages                                                                                                                                                                                                                                                   |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **People**   | **Users**: every account, its role (standard or system admin), deletion and, since v1.19.0, [Add user](#add-a-user). **Groups** (v1.18.0+): see [Groups](https://depictio.github.io/depictio-docs/latest/usage/administration/groups/#managing-a-group) |
| **Content**  | **Projects** and **Dashboards**: every one of them, whoever owns it. Admins can delete any                                                                                                                                                              |
| **Activity** | **Tasks**, **Ingestion**, **Watchers**, **Logs** and **Health**, see [Monitoring](https://depictio.github.io/depictio-docs/latest/usage/administration/monitoring/index.md)                                                                             |
| **Instance** | [**Branding**](https://depictio.github.io/depictio-docs/latest/usage/administration/branding/index.md), [**Backups**](https://depictio.github.io/depictio-docs/latest/usage/administration/backup/index.md), **Maintenance** and **Settings**           |

### Adding a user (v1.19.0+)

**Administration → Users → Add user** creates an account with an email, a display name and an initial password, generated by default (with refresh and copy). Two switches: **ask for a new password at first sign-in**, on by default, and **system admin**. A person asked to change it is taken to the Password section of Account settings until they do, and the Users list shows the pending change.

It works even when [registration](https://depictio.github.io/depictio-docs/latest/usage/guides/authentication-modes/#registration) or [password sign-in](https://depictio.github.io/depictio-docs/latest/usage/guides/authentication-modes/#password-login) is closed: on an SSO-only instance the account is matched by email at the first SSO sign-in, which is how a person is added to a [group](https://depictio.github.io/depictio-docs/latest/usage/administration/groups/index.md) before they ever sign in. It is not offered in single-user or public mode.

### Release check (v1.17.0+)

**Administration → Settings → Version check** tells administrators when a newer Depictio release is published. The server asks the GitHub Releases API of `depictio/depictio` every 6 hours, with a plain request that sends nothing about the instance, and the [server information](#server-information) shows the result to administrators only. **Check now** asks at once.

The check is on by default and the switch turns it off for the instance. Setting [`DEPICTIO_VERSION_CHECK_ENABLED`](https://depictio.github.io/depictio-docs/latest/installation/env-reference/#release-check) to `true` or `false` decides instead and locks the switch, for instances that must make no outbound call.

Since v1.18.0 the check also runs as soon as the running version is not the one that last checked, so the page never shows a latest release older than the current one after an upgrade.

## Page reference

Depictio's main pages and their URLs:

### Projects list (/projects)

### Project detail (/projects/{id})

A single project's data. Since v1.17.0 the page starts with a sentence on what the project holds and its workflows, as cards to pick one from, then a switch between two views:

- **Data collections** — the project's workflows, a sortable, filterable table of its data collections, its cross-DC links, and the details of the selected collection. For a [composed](https://depictio.github.io/depictio-docs/latest/usage/projects/composed-dashboards/index.md) project, a **Files the catalog did not recognise** card lists the tables left out, with the command that adds each (v1.16.0+).
- **Ingestion** — the [ingestion report](https://depictio.github.io/depictio-docs/latest/features/dashboards/#ingestion-report-health), offered for **every** project since v1.6.0. For one created from a [pipeline template](https://depictio.github.io/depictio-docs/latest/pipeline-templates/index.md) it compares expected against ingested data collections; for any other it reads the collections the project declares today, and a **Live project** badge says so. Since v1.15.0 a **History** view lists the project's [ingestion runs](https://depictio.github.io/depictio-docs/latest/features/dashboards/#ingestion-history), and, where the server allows it, [**Run ingestion**](https://depictio.github.io/depictio-docs/latest/features/dashboards/#run-ingestion) starts one from the browser.

Selecting a data collection shows its details, including its **Delta version**, and for a table a data preview and its **Version history**: see [Dataset history](https://depictio.github.io/depictio-docs/latest/features/versioning/#dataset-history).

You can reach this page directly by clicking the **project badge** shown on any dashboard card or in the dashboards table, or the **project name** in an open dashboard's Settings (v1.6.0+).

Data that is not on the server's own disk is handled in two places (v1.16.0+); the mechanisms are described on [Remote data and manifests](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/index.md).

- **Remote URL** in **Create Data Collection**: the **Table (CSV / TSV / Parquet)** tab offers **Upload a file** or **Remote URL**. With the latter, paste an `https://` or `s3://` address as the **File URL** (`http://` only when the server allows it); the name and format are filled in from its last segment. The server fetches the file, so it never travels through the browser, and a private bucket is read with the project's storage settings. MultiQC reports are uploaded only.
- **Project settings** in the header, next to **Permissions**, opens three sections; nothing is saved on close, each acts on its own button:
  - **Storage**, for project owners and administrators: the endpoint, bucket, region and keys of a private bucket the project reads, with **Test connection**. See [Project storage settings](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#project-storage-settings).
  - **Data refresh**: re-read the collections that come from a manifest, a URL or a bucket, and rebuild their tables. See [Refreshing the data](https://depictio.github.io/depictio-docs/latest/usage/projects/remote-data/#refreshing-the-data).
  - **Export**: package the project and its dashboards as a template bundle (zip). See [Export a project as a template](https://depictio.github.io/depictio-docs/latest/usage/projects/templates/#export-a-project-as-a-template).

**Data refresh** and **Export** are for owners, editors and administrators; on a public instance, administrators only. The dialog opens on the section used last.

### Dashboard viewer (/dashboard/{id})

Read-only dashboard with filters and component interactions.

### Dashboard editor (/dashboard-edit/{id})

Design mode — add, configure, and arrange components.

### CLI agents / tokens (/profile#cli-agents)

Generate and manage CLI configurations for the [`depictio` CLI](https://depictio.github.io/depictio-docs/latest/depictio-cli/usage/index.md). Saved as `~/.depictio/CLI.yaml`, a configuration is the server every CLI command uses by default. Since v1.17.0 they are a section of [Account settings](#account-settings), and `/cli-agents` leads there.
