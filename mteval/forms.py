from wtforms import Form, StringField, PasswordField, validators

MIN_TEAM_NAME = 3
MAX_TEAM_NAME = 30
MIN_PASS = 6
MAX_PASS = 80


class LoginForm(Form):
	teamname = StringField("Team name", [validators.Required("Team name / email required"), 
		validators.Length(min=MIN_TEAM_NAME, max=MAX_TEAM_NAME)])
	password = PasswordField("Password", [validators.Required("Password required"), 
		validators.Length(min=MIN_PASS, max=MAX_PASS)])

class RegisterForm(Form):
	teamname = StringField("Team name", [validators.Required("Team name required"), 
		validators.Length(min=MIN_TEAM_NAME, max=MAX_TEAM_NAME)])
	email = StringField("Email", [validators.Required("Email required"),validators.Email()])
	organisation = StringField("Organisation")
	password = PasswordField("Password", [validators.Required("Password required"), 
		validators.EqualTo("confirm", message="Passwords must match"), validators.Length(min=MIN_PASS, max=MAX_PASS)])
	confirm = PasswordField("Repeat password")

class EditTeamForm(Form):
	teamname = StringField("Team name", [validators.Required("Team name required"),	validators.Length(min=MIN_TEAM_NAME, max=MAX_TEAM_NAME)])
	email = StringField("Email", [validators.Required("Email required"),validators.Email()])
	organisation = StringField("Organisation")