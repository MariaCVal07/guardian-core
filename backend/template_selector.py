from templates.login_template import LOGIN_TEMPLATE

class TemplateSelector:

    def select_template(self, requirement):

        requirement = requirement.lower()

        if "login" in requirement:

            return LOGIN_TEMPLATE

        return None
