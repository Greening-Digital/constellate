import webbrowser


def view_rendered_html_in_browser(string_template):
    """
    Accepts a string, containing generated HTML template
    then opens it in the default browser on a computer
    """

    # show the rendered html
    with open("email_test.html", "w+") as f:
        f.write(string_template)

    webbrowser.open("email_test.html")
