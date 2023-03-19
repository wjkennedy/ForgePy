import os
import subprocess
import ipywidgets as widgets
from IPython.display import display

# Install the Forge CLI
subprocess.run(["npm", "install", "-g", "@forge/cli"])

# Function to create a new Forge app
def create_forge_app(app_name, app_url):
    subprocess.run(["forge", "create", app_name, "--default-auth", "jwt", "--url", app_url])

    # Navigate to the app directory
    os.chdir(app_name)

    # Add the necessary permissions and modules to the app's manifest file
    with open("app/manifest.yml", "a") as manifest_file:
        manifest_file.write("""
permissions:
  scopes:
    - 'read:jira-work'
    - 'write:jira-work'

modules:
  jira:webhooks:
    - event: jira:issue_created
      url: https://<your-app-domain>/create-ticket
""")

    # Create a new endpoint for creating Jira tickets
    with open("app/src/index.js", "a") as index_file:
        index_file.write("""
app.post('/create-ticket', async (req, res) => {
    // Add your Jira ticket creation logic here
});
""")

    # Deploy the app to the Forge platform
    subprocess.run(["forge", "deploy"])

# Function to export the Forge app resources
def export_forge_resources(app_name):
    subprocess.run(["forge", "export", app_name, "--zip"])

# Create widgets for accepting user input
app_name_widget = widgets.Text(description="App Name:")
app_url_widget = widgets.Text(description="App URL:")

# Create buttons for creating the app and exporting resources
create_app_button = widgets.Button(description="Create App")
export_resources_button = widgets.Button(description="Export Resources")

# Create functions to handle button clicks
def create_app_button_clicked(b):
    create_forge_app(app_name_widget.value, app_url_widget.value)

def export_resources_button_clicked(b):
    export_forge_resources(app_name_widget.value + ".zip")

# Attach button click handlers to buttons
create_app_button.on_click(create_app_button_clicked)
export_resources_button.on_click(export_resources_button_clicked)

# Display the widgets and buttons
display(app_name_widget, app_url_widget)
display(create_app_button, export_resources_button)
