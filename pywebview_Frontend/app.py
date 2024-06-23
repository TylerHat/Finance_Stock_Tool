import webview
from bollingBandsRSI import bollingBandsRSI_test

# Define a function to create the webview window
def create_window():

    html_result = bollingBandsRSI_test("META", 100)
    # Create a window with a title and load the HTML file
    window = webview.create_window('Pywebview Example',html_result)
    # Start the webview event loop
    webview.start()

# Entry point of the script
if __name__ == '__main__':
    create_window()
