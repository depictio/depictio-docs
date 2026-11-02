# <span style="color: #F68B33;">:material-web:</span> Web UI

## <span style="color: #9966CC;">:material-palette-swatch-outline:</span> Paper and Classic <small>(v1.17.0+)</small> { #looks }

Depictio comes in two looks, with the same pages, panels and settings:

- **Paper**, the default since v1.17.0: every page on paper panels, a top bar with the
  page or dashboard title, and a sidebar. On a dashboard, the tab sidebar folds to an icon
  rail, by itself while the filter panel is open, and a floating **dock** holds Search,
  Analysis, Comments and Edit / Save / Exit as icon keys. Drag it by its grip, or use the
  arrow keys, to the bottom, left, right or top of the page; the browser keeps the place.
- **Classic**, the layout of earlier versions: a header bar of buttons and a tab sidebar.

=== "Paper"

    [![The Iris dashboard in the Paper look: the title and a breadcrumb in the top bar, the tab rail and the filter panel on the left, the Overview tab, and the dock at the bottom](../../images/guides/web-ui/look_paper_light.webp#only-light)](../../images/guides/web-ui/look_paper_light.webp){target=_blank}
    [![The Iris dashboard in the Paper look: the title and a breadcrumb in the top bar, the tab rail and the filter panel on the left, the Overview tab, and the dock at the bottom](../../images/guides/web-ui/look_paper_dark.webp#only-dark)](../../images/guides/web-ui/look_paper_dark.webp){target=_blank}

=== "Classic"

    [![The same dashboard in the Classic look: a header bar with Comments, Analysis, Edit and Settings, the tab sidebar, the filter panel and the Overview tab](../../images/guides/web-ui/look_classic_light.webp#only-light)](../../images/guides/web-ui/look_classic_light.webp){target=_blank}
    [![The same dashboard in the Classic look: a header bar with Comments, Analysis, Edit and Settings, the tab sidebar, the filter panel and the Overview tab](../../images/guides/web-ui/look_classic_dark.webp#only-dark)](../../images/guides/web-ui/look_classic_dark.webp){target=_blank}

A page takes the first of:

1. `?chrome=glass` (Paper) or `?chrome=base` (Classic) in its URL, kept for the rest of
   the browser session, for support and testing;
2. your own pick, in [**Account settings → Preferences → Look**](#account-settings), kept
   in this browser;
3. the default an administrator sets in
   [**Administration → Branding → Default look**](../administration/branding.md#default-look);
4. Paper.

Screenshots in these docs show one look or the other; where a control sits in the header
in Classic, Paper has it in the top bar or the dock.

## <span style="color: #8BC34A;">:material-account-plus:</span> Register and login

### <span style="color: #6495ED;">:material-account-plus:</span> Registering an Account (Sign Up)

1. **Navigate to the Registration page** by clicking the **Register** button on the login screen.

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/register_login/login.png" target="_blank">
        <img src="../../../images/guides/register_login/login.png" width="600">
    </a>
</div>

2. **Enter your email address** in the "Email" field.

3. **Create a password** and enter it in the "Password" field. You can click the eye icon to view the password as you type and **Confirm your password** by re-entering it in the "Confirm Password" field.

4. Click the **Register** button to submit your registration details.

5. After successful registration, you can return to the login page by clicking the **Back to Login** button.

### <span style="color: #45B8AC;">:material-login:</span> Logging In (Sign In)

1. **Open the Depictio Login page**.
2. **Enter your email address** in the "Email" field.
3. **Enter your password** in the "Password" field.
4. If you want to see the password as you type it, click the eye icon next to the password field.
5. Once both fields are filled in, click the **Login** button.
6. You will be redirected to the Depictio landing page (currently `/dashboards`).

### <span style="color: #E53935;">:material-google:</span> Google OAuth Login

If you have configured Google OAuth for your Depictio instance (see [Configuration](../../../installation/configuration/#google-oauth-integration)), you can log in using your Google account. If the account does not exist, it will be created automatically.

When the server refuses the sign-in, for example because registration is closed, the
callback page shows **Sign-in failed** and the reason, since v1.17.2.

### <span style="color: #1E88E5;">:material-shield-key-outline:</span> SSO login <small>(v1.18.0+)</small>

An instance with [SAML single sign-on](../../installation/sso.md) adds a button, *Sign in
with SSO* or the label it sets, that sends you to your institution's identity provider and
back.

## <span style="color: #F68B33;">:material-view-dashboard:</span> Landing page / Dashboards section (/dashboards) { #dashboards-listing }

[![The Dashboards page in the Paper look: the toolbar with search, sections and display menus, and the table of dashboards](../../images/guides/web-ui/dashboards_light.webp#only-light)](../../images/guides/web-ui/dashboards_light.webp){target=_blank}
[![The Dashboards page in the Paper look: the toolbar with search, sections and display menus, and the table of dashboards](../../images/guides/web-ui/dashboards_dark.webp#only-dark)](../../images/guides/web-ui/dashboards_dark.webp){target=_blank}

The listing opens on the **Table** view <small>(v1.12.0+)</small>, one row per dashboard. In the
**Thumbnails** view each dashboard is shown as a card. Cards display the dashboard's screenshot thumbnail
once one has been captured, and fall back to the dashboard's logo (when set) before the
generic placeholder.

The table view has a **Last viewed** column <small>(v1.11.0+)</small>, sorted newest
first, with dashboards you never opened last. It is kept per browser.

The **Table display** menu <small>(v1.17.0+)</small> sets the row height, **Comfortable**
or **Compact**, and which columns show, with **Show all** and **Reset**. The Projects
listing has the same menu. On a narrow screen the actions column stays pinned to the
right edge while the table scrolls <small>(v1.17.3+)</small>.

Dashboards are grouped into sections, each dashboard in one only, in this order:
**nf-core dashboards**, **Demo dashboards**, **Public**, **Accessed** and **Owned**.
Since v1.17.2 the nf-core section holds every dashboard of an nf-core workflow, the
imported templates included: the seeded ones first, then the others by title.

#### <span style="color: #45B8AC;">:material-view-grid-outline:</span> Thumbnails or table <small>(v1.11.2+)</small> { #listing-views }

The view switcher in the toolbar picks between **Thumbnails**, the card grid, and
**Table**, with sortable columns and bulk selection. The Tiles view of earlier
versions is gone, and a browser that had it opens on Thumbnails.

In Thumbnails, the **Card display** menu beside the switcher sets:

- **Cards per row**: 5 by default since v1.12.0, or 2 to 6, or Auto. Auto never makes
  more columns than a section has cards, so a section with a single dashboard draws
  it across the whole width.
- **Badges**: which of Project, Template, Owner, Visibility, Last modified and Tabs a
  card shows. Hovering a badge gives its long form.

**Reset to defaults** restores both, so five cards per row. They are layout preferences,
kept in the browser and left out of shared links. A browser that opened the listing
before v1.12.0 stored Auto, the former default, and keeps it until you pick another
value or reset. Resting the pointer on a thumbnail opens a larger,
sharper preview.

Someone who never picked a view gets the one the deployment sets with
[`DEPICTIO_VIEWER_DASHBOARDS_DEFAULT_VIEW`](../../installation/env-reference.md#react-viewer-frontend):
**Table** since v1.12.0, Thumbnails before. Set it to `thumbnails` to open the grid
again. A view picked in the browser, or named by a shared link such as
`/dashboards?view=thumbnails`, wins over it.

### <span style="color: #7A5DC7;">:material-menu:</span> Sidebar Navigation

The left sidebar provides easy access to various sections of the application. This includes:

- <span style="color: #F68B33;">:material-view-dashboard:</span> **Dashboards**: View and manage your dashboards.
- <span style="color: #45B8AC;">:material-folder-multiple:</span> **Projects**: Manage your projects and data collections.
- <span style="color: #E53935;">:material-shield-account:</span> **Administration** (sysadmin users only): Access administrative features (only available to users with admin privileges).
- <span style="color: #6495ED;">:material-information:</span> **About**: Information about the application and its repository.

The button at the top of the sidebar folds it to icons. The top bar holds the theme
toggle and your avatar, which opens [Account settings](#account-settings) <small>(v1.17.0+)</small>.
The compass in the header of the Dashboards and Projects pages starts the guided tour.

#### <span style="color: #45B8AC;">:material-server-outline:</span> Server information <small>(v1.17.0+)</small> { #server-information }

The server status at the foot of the sidebar, **Online** with the server version, opens
the server information: version, API, mode, and links to the documentation, GitHub, the
releases and the issue tracker. On a dashboard it sits at the foot of the tab rail, and
in Classic it is the version badge.

[![The server information popover open from the sidebar status: Depictio server online, version v1.17.1, API v1, single-user mode, four links, and Up to date, checked 17 minutes ago](../../images/guides/web-ui/server_info_light.webp#only-light)](../../images/guides/web-ui/server_info_light.webp){target=_blank}
[![The server information popover open from the sidebar status: Depictio server online, version v1.17.1, API v1, single-user mode, four links, and Up to date, checked 17 minutes ago](../../images/guides/web-ui/server_info_dark.webp#only-dark)](../../images/guides/web-ui/server_info_dark.webp){target=_blank}

For administrators, its last line says whether a newer Depictio release is out. When one
is, a dot marks the status and a card in the popover names the release; **OK** hides it
until the next one. See [Release check](#release-check).

### <span style="color: #F68B33;">:material-plus-circle:</span> Creating a New Dashboard

1. On the **landing page**, click the orange **"+ New Dashboard"** button located in the top right corner.
2. A pop-up window will appear with a field labeled **"Dashboard Title"**.
3. **Enter a name** for your new dashboard.
4. Your dashboard will be created with the title you provided and added to the section.
5. Click the blue **"Create Dashboard"** button to create the dashboard.
6. The new dashboard will appear in the section with informations including name, owner and status (public/private).

### <span style="color: #9966CC;">:material-cog:</span> Functionalities

#### <span style="color: #6495ED;">:material-eye:</span> Viewing a Dashboard

1. Once a dashboard is created, it will appear under the section.
2. Click the **"View"** button next to the dashboard name to open and explore its content.

#### <span style="color: #E53935;">:material-delete:</span> Deleting a Dashboard

1. To delete a dashboard, locate the dashboard in the section.
2. Click the red **"Delete"** button next to the dashboard name.
3. A confirmation pop-up will appear, asking **"Are you sure you want to delete this dashboard?"**.
4. Click **"Delete"** to permanently remove the dashboard, or **"Cancel"** to keep it.

#### <span style="color: #F9CB40;">:material-pencil:</span> Editing dashboard name

1. To edit the name of a dashboard, locate the dashboard in the section.
2. Click the **"Edit name"** button next to the dashboard name.
3. A pop-up window will appear with a field labeled **"New name"**.
4. **Enter a new name** for your dashboard.
5. Click the blue **"Save"** button to save the new name.

#### <span style="color: #7A5DC7;">:material-content-copy:</span> Duplicating a dashboard

1. To duplicate a dashboard, locate the dashboard in the section.
2. Click the **"Duplicate"** button next to the dashboard name.
3. The dashboard will be duplicated and added to the section with the suffix **"(copy)"**.

!!! note
    <div style="border: 0px solid grey; padding: 1px; text-align: center;">
    <a href="../../../images/guides/dashboard_creation/dashboard_status.png" target="_blank">
    <img src="../../../images/guides/dashboard_creation/dashboard_status.png" width="100">
    </a>
    </div>
    Both "public" and "private" dashboards are listed in the **Dashboards** section. Public dashboards are accessible to all users, while private dashboards are only visible to the user who created them.
    Only the user who created a private dashboard can edit, or delete it.

#### <span style="color: #45B8AC;">:material-link-variant:</span> Share a filtered listing <small>(v1.10.1+)</small> { #share-a-filtered-listing }

The filters of `/dashboards` and `/projects` are kept in the URL. Set them, then
press the link button in the toolbar to copy a link to that view:

| Link | Shows |
| --- | --- |
| `/dashboards?template=nf-core/rnaseq` | Dashboards built from nf-core/rnaseq, any version |
| `/projects?template=nf-core/rnaseq,nf-core/viralrecon` | Projects built from either pipeline |

Whoever opens it sees a **Shared view** banner, with **Show everything** to clear the
filters. The link grants no access: it only narrows what they could already open.

## <span style="color: #45B8AC;">:material-folder-multiple:</span> Projects section (/projects)


!!! info "Complete Projects Documentation"
    **For comprehensive information about Projects in Depictio, see the dedicated [Projects Guide](../projects/guide.md).**

    The Projects Guide covers:

    - **Project Types** - Basic vs Advanced projects
    - **Creating Projects** - Step-by-step instructions
    - **Configuration** - YAML setup and examples
    - **Data Collections** - File organization and processing
    - **Permissions** - Access control and collaboration
    - **Best Practices** - Optimization and troubleshooting

    **Quick Links:**

    - :material-folder-multiple: **[Projects Guide](../projects/guide.md)** - Complete project management
    - :material-code-braces: **[YAML Examples](../projects/yaml-examples.md)** - Configuration patterns
    - :material-file-document: **[Configuration Reference](../projects/reference.md)** - Full parameter reference


### <span style="color: #6495ED;">:material-information:</span> Quick Overview

- The left sidebar includes a **"Projects"** section where users can manage their projects
- Click on **"Projects"** to navigate and view them
- Projects organize your data and provide structure for dashboards
- You can access workflows and data collections recursively within each project
- Each entity allows you to view configuration details and preview data

### <span style="color: #45B8AC;">:material-link-variant:</span> Creating a project from a run folder or a manifest <small>(v1.16.0+)</small> { #creating-a-project-from-a-manifest }

**+ New Project** offers four tabs: **Create New**, **Import**, **From
Manifest** and **From a run folder**. The last two build a project from data
the server reads, with no CLI involved, in three steps: **Source**, **Preview**
(a dry run, nothing is created) and **Create**.

- **From a run folder**: point at the results folder of one pipeline run, in a
  bucket or, on a `depictio local` server, on this computer. Depictio
  recognises the pipeline, picks the template and shows what each data
  collection finds there; the data is ingested in the background. See
  [From a run folder](../projects/remote-data.md#from-a-run-folder).
- **From Manifest**: paste the URL of a
  [data manifest](../projects/remote-data.md#the-data-manifest-contract) and
  pick a template that reads one. See
  [From a manifest](../projects/remote-data.md#creating-a-project-from-a-manifest).

## <span style="color: #8BC34A;">:material-account:</span> Account settings (/profile) <small>(v1.17.0+)</small> { #account-settings }

Your avatar in the top bar opens **Account settings**, one page of sections that open
and close:

- **Account**: your email, role and dates. Click the avatar to upload a profile
  picture; the server stores it as a 256-pixel WebP and includes it in
  [backups](../administration/backup.md). Signing in with Google sets your Google picture
  until you upload one.
  Since v1.18.0 it shows your [group](../administration/groups.md#my-groups) badges
  (crown for P.I., shield for group admin), which open `/groups`, and the name and title
  your identity provider gives.
- **Password**: change the password you sign in with.
- **CLI agents**: the long-lived tokens of the `depictio` command line, see
  [Create a CLI configuration](../get_started.md#create-a-cli-configuration). The former
  `/cli-agents` page leads here.
- **Preferences**, kept in this browser: **Theme**, light or dark; [**Look**](#looks),
  Paper, Classic or the instance default; **Font size** of figures, tables and cards.
- **Getting started**: replay the guided tour of the app or of the builder.
- **Server**: the [server information](#server-information).

**Sign out** is at the foot of the page.

=== "Account"

    [![Account settings: the Account section open, with the avatar, email, role, database ID and dates, then the Password, CLI agents, Preferences, Getting started and Server sections](../../images/guides/web-ui/account_settings_light.webp#only-light)](../../images/guides/web-ui/account_settings_light.webp){target=_blank}
    [![Account settings: the Account section open, with the avatar, email, role, database ID and dates, then the Password, CLI agents, Preferences, Getting started and Server sections](../../images/guides/web-ui/account_settings_dark.webp#only-dark)](../../images/guides/web-ui/account_settings_dark.webp){target=_blank}

=== "Preferences"

    [![The Preferences section open: Theme Light or Dark, Look with Instance default (Paper), Paper and Classic, and Font size at 100%](../../images/guides/web-ui/account_preferences_light.webp#only-light)](../../images/guides/web-ui/account_preferences_light.webp){target=_blank}
    [![The Preferences section open: Theme Light or Dark, Look with Instance default (Paper), Paper and Classic, and Font size at 100%](../../images/guides/web-ui/account_preferences_dark.webp#only-dark)](../../images/guides/web-ui/account_preferences_dark.webp){target=_blank}

## <span style="color: #6495ED;">:material-information:</span> About section (/about)

[![The About page: GitHub repository and documentation cards, then the funding cards](../../images/guides/web-ui/about_light.webp#only-light)](../../images/guides/web-ui/about_light.webp){target=_blank}
[![The About page: GitHub repository and documentation cards, then the funding cards](../../images/guides/web-ui/about_dark.webp#only-dark)](../../images/guides/web-ui/about_dark.webp){target=_blank}

The **About** section provides information about the GitHub repository and the documentation.

## <span style="color: #E53935;">:material-shield-account:</span> Admin section (/admin) { #admin-section }

[![Administration in the Paper look, its pages grouped under People, Content, Activity and Instance](../../images/guides/web-ui/admin_default_look_light.webp#only-light)](../../images/guides/web-ui/admin_default_look_light.webp){target=_blank}
[![Administration in the Paper look, its pages grouped under People, Content, Activity and Instance](../../images/guides/web-ui/admin_default_look_dark.webp#only-dark)](../../images/guides/web-ui/admin_default_look_dark.webp){target=_blank}

The **Admin** section is only accessible to users with admin privileges. Since v1.17.0
its pages are listed down the side, in four groups:

| Group | Pages |
|-------|-------|
| **People** | **Users**: every account, its role (standard or system admin), deletion and, since v1.19.0, [Add user](#add-a-user). **Groups** <small>(v1.18.0+)</small>: see [Groups](../administration/groups.md#managing-a-group) |
| **Content** | **Projects** and **Dashboards**: every one of them, whoever owns it. Admins can delete any |
| **Activity** | **Tasks**, **Ingestion**, **Watchers**, **Logs** and **Health**, see [Monitoring](../administration/monitoring.md) |
| **Instance** | [**Branding**](../administration/branding.md), [**Backups**](../administration/backup.md), **Maintenance** and **Settings** |

### <span style="color: #E53935;">:material-account-plus-outline:</span> Adding a user <small>(v1.19.0+)</small> { #add-a-user }

**Administration → Users → Add user** creates an account with an email, a display name and
an initial password, generated by default (with refresh and copy). Two switches: **ask for a
new password at first sign-in**, on by default, and **system admin**. A person asked to
change it is taken to the Password section of Account settings until they do, and the Users
list shows the pending change.

It works even when [registration](authentication-modes.md#registration) or
[password sign-in](authentication-modes.md#password-login) is closed: on an SSO-only
instance the account is matched by email at the first SSO sign-in, which is how a person is
added to a [group](../administration/groups.md) before they ever sign in. It is not offered
in single-user or public mode.

### <span style="color: #E53935;">:material-update:</span> Release check <small>(v1.17.0+)</small> { #release-check }

**Administration → Settings → Version check** tells administrators when a newer Depictio
release is published. The server asks the GitHub Releases API of `depictio/depictio`
every 6 hours, with a plain request that sends nothing about the instance, and the
[server information](#server-information) shows the result to administrators only.
**Check now** asks at once.

[![Administration, Settings: the Version check card with Check for new versions on, checks every 6 h, repository depictio/depictio, current version and latest release 1.17.1, and the Reset to default, Check now and Save buttons](../../images/guides/web-ui/admin_settings_light.webp#only-light)](../../images/guides/web-ui/admin_settings_light.webp){target=_blank}
[![Administration, Settings: the Version check card with Check for new versions on, checks every 6 h, repository depictio/depictio, current version and latest release 1.17.1, and the Reset to default, Check now and Save buttons](../../images/guides/web-ui/admin_settings_dark.webp#only-dark)](../../images/guides/web-ui/admin_settings_dark.webp){target=_blank}

The check is on by default and the switch turns it off for the instance. Setting
[`DEPICTIO_VERSION_CHECK_ENABLED`](../../installation/env-reference.md#release-check) to
`true` or `false` decides instead and locks the switch, for instances that must make no
outbound call.

Since v1.18.0 the check also runs as soon as the running version is not the one that last
checked, so the page never shows a latest release older than the current one after an
upgrade.

## <span style="color: #45B8AC;">:material-sitemap:</span> Page reference

Depictio's main pages and their URLs:

### <span style="color: #45B8AC;">:material-folder-multiple:</span> Projects list (/projects)

[![The Projects page: the toolbar and the table of projects with type, visibility, template, owner, workflows and data collections](../../images/guides/web-ui/projects_light.webp#only-light)](../../images/guides/web-ui/projects_light.webp){target=_blank}
[![The Projects page: the toolbar and the table of projects with type, visibility, template, owner, workflows and data collections](../../images/guides/web-ui/projects_dark.webp#only-dark)](../../images/guides/web-ui/projects_dark.webp){target=_blank}

### <span style="color: #45B8AC;">:material-database-cog:</span> Project detail (/projects/{id}) { #project-detail }

A single project's data. Since v1.17.0 the page starts with the project's type and its
workflows, as cards to pick one from, then a switch between two views:

- **Data collections** — the project's workflows, a sortable, filterable table of its data collections, its cross-DC links, and the details of the selected collection. For a [composed](../projects/composed-dashboards.md) project, a **Files the catalog did not recognise** card lists the tables left out, with the command that adds each <small>(v1.16.0+)</small>.
- **Ingestion** — the [ingestion report](../../features/dashboards.md#ingestion-report-health), offered for **every** project since v1.6.0. For one created from a [pipeline template](../../pipeline-templates/README.md) it compares expected against ingested data collections; for any other it reads the collections the project declares today, and a **Live project** badge says so. Since v1.15.0 a **History** view lists the project's [ingestion runs](../../features/dashboards.md#ingestion-history), and, where the server allows it, [**Run ingestion**](../../features/dashboards.md#run-ingestion) starts one from the browser.

Selecting a data collection shows its details, including its **Delta version**, and for a
table a data preview and its **Version history**: see
[Dataset history](../../features/versioning.md#dataset-history).

You can reach this page directly by clicking the **project badge** shown on any
dashboard card or in the dashboards table, or the **project name** in an open
dashboard's Settings <small>(v1.6.0+)</small>.

[![A project page: type Advanced, the penguin_species_analysis workflow selected, and the switch between Data collections and Ingestion report, on Data collections](../../images/guides/web-ui/project_detail_light.webp#only-light)](../../images/guides/web-ui/project_detail_light.webp){target=_blank}
[![A project page: type Advanced, the penguin_species_analysis workflow selected, and the switch between Data collections and Ingestion report, on Data collections](../../images/guides/web-ui/project_detail_dark.webp#only-dark)](../../images/guides/web-ui/project_detail_dark.webp){target=_blank}

Data that is not on the server's own disk is handled in two places
<small>(v1.16.0+)</small>; the mechanisms are described on
[Remote data and manifests](../projects/remote-data.md).

- **Remote URL** in **Create Data Collection**: the **Table (CSV / TSV /
  Parquet)** tab offers **Upload a file** or **Remote URL**. With the latter,
  paste an `https://` or `s3://` address as the **File URL** (`http://` only
  when the server allows it); the name and format are filled in from its last
  segment. The server fetches the file, so it never travels through the
  browser, and a private bucket is read with the project's storage settings.
  MultiQC reports are uploaded only.
- **Project settings** in the header, next to **Permissions**, opens three
  sections; nothing is saved on close, each acts on its own button:
    - **Storage**, for project owners and administrators: the endpoint,
      bucket, region and keys of a private bucket the project reads, with
      **Test connection**. See
      [Project storage settings](../projects/remote-data.md#project-storage-settings).
    - **Data refresh**: re-read the collections that come from a manifest, a
      URL or a bucket, and rebuild their tables. See
      [Refreshing the data](../projects/remote-data.md#refreshing-the-data).
    - **Export**: package the project and its dashboards as a template bundle
      (zip). See
      [Export a project as a template](../projects/templates.md#export-a-project-as-a-template).

  **Data refresh** and **Export** are for owners, editors and administrators;
  on a public instance, administrators only. The dialog opens on the section
  used last.

### <span style="color: #45B8AC;">:material-monitor-eye:</span> Dashboard viewer (/dashboard/{id})

Read-only dashboard with filters and component interactions.

[![The Iris dashboard in the viewer](../../images/guides/web-ui/look_paper_light.webp#only-light)](../../images/guides/web-ui/look_paper_light.webp){target=_blank}
[![The Iris dashboard in the viewer](../../images/guides/web-ui/look_paper_dark.webp#only-dark)](../../images/guides/web-ui/look_paper_dark.webp){target=_blank}

### <span style="color: #45B8AC;">:material-pencil-ruler:</span> Dashboard editor (/dashboard-edit/{id})

Design mode — add, configure, and arrange components.

[![The Iris dashboard in the editor: an Editing badge next to the title, and the dock with Add, Save and the other editing keys](../../images/guides/web-ui/editor_light.webp#only-light)](../../images/guides/web-ui/editor_light.webp){target=_blank}
[![The Iris dashboard in the editor: an Editing badge next to the title, and the dock with Add, Save and the other editing keys](../../images/guides/web-ui/editor_dark.webp#only-dark)](../../images/guides/web-ui/editor_dark.webp){target=_blank}

### <span style="color: #45B8AC;">:material-key-chain:</span> CLI agents / tokens (/profile#cli-agents)

Generate and manage CLI configurations for the [`depictio` CLI](../../depictio-cli/usage.md). Saved as `~/.depictio/CLI.yaml`, a configuration is the server every CLI command uses by default. Since v1.17.0 they are a section of [Account settings](#account-settings), and `/cli-agents` leads there.

[![The CLI agents section of Account settings: Add configuration, and two configurations, default_token and laptop, each with its expiry date and Delete](../../images/guides/web-ui/cli_agents_light.webp#only-light)](../../images/guides/web-ui/cli_agents_light.webp){target=_blank}
[![The CLI agents section of Account settings: Add configuration, and two configurations, default_token and laptop, each with its expiry date and Delete](../../images/guides/web-ui/cli_agents_dark.webp#only-dark)](../../images/guides/web-ui/cli_agents_dark.webp){target=_blank}
