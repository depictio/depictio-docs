# <span style="color: #F68B33;">:material-web:</span> Web UI

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

## <span style="color: #F68B33;">:material-view-dashboard:</span> Landing page / Dashboards section (/dashboards)

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/pages/landing_page.png" target="_blank">
        <img src="../../../images/guides/pages/landing_page.png" width="600">
    </a>
</div>

### <span style="color: #7A5DC7;">:material-menu:</span> Sidebar Navigation

The left sidebar provides easy access to various sections of the application. This includes:

- <span style="color: #F68B33;">:material-view-dashboard:</span> **Dashboards**: View and manage your dashboards.
- <span style="color: #45B8AC;">:material-folder-multiple:</span> **Projects**: Manage your projects and data collections.
- <span style="color: #E53935;">:material-shield-account:</span> **Administration** (sysadmin users only): Access administrative features (only available to users with admin privileges).
- <span style="color: #6495ED;">:material-information:</span> **About**: Information about the application and its repository.
- <span style="color: #8BC34A;">:material-account:</span> **Profile**: View and edit your user profile by clicking on the avatar icon in the bottom left corner.

At the bottom of the sidebar, you will find:

  - **Theme toggle**: Switch between light and dark themes.
  - **Server status**: Displays the current server version and online status.
  - **User information**: Displays your username and email (e.g., `test_user@example.com`).

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

## <span style="color: #8BC34A;">:material-account:</span> User Information (/profile)

You can access your user profile by clicking on the avatar icon in the bottom left corner of the sidebar.

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/pages/profile.png" target="_blank">
        <img src="../../../images/guides/pages/profile.png" width="600">
    </a>
</div>

This section allows you to:

- View your username and email address
- Edit your password
- Generate CLI Configurations for command-line access (see [CLI Usage](../get_started.md#create-a-cli-configuration))

## <span style="color: #6495ED;">:material-information:</span> About section (/about)

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/pages/about.png" target="_blank">
        <img src="../../../images/guides/pages/about.png" width="600">
    </a>
</div>

The **About** section provides information about the GitHub repository and the documentation.

## <span style="color: #E53935;">:material-shield-account:</span> Admin section (/admin)

<div style="border: 1px solid grey; width: 602px; padding: 1px;">
    <a href="../../../images/guides/pages/admin_users.png" target="_blank">
        <img src="../../../images/guides/pages/admin_users.png" width="600">
    </a>
</div>

The **Admin** section is only accessible to users with admin privileges. It allows admins to view users, projects and dashboards. The **Users** tab displays a list/delete/change status (sysadmin/standard) of all users registered in the system. The **Dashboards** tab displays a list of all dashboards while the **Projects** tab lists all projects. Admins can delete any project or dashboard, regardless of ownership.
