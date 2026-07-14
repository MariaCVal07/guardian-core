from backend.templates.login_template import LOGIN_TEMPLATE


class TemplateSelector:

    def __init__(self):

        self.templates = {

            "login": LOGIN_TEMPLATE
        }

    def select_template(
        self,
        requirement
    ):

        requirement = requirement.lower()

        for keyword, template in self.templates.items():

            if keyword in requirement:

                return template

        return None
