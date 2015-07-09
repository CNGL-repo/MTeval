from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
	teamname = StringField("Team name", [validators.Required()])
	password = PasswordField("Password", [validators.Required()])

class RegisterForm(Form):
	teamname = StringField("Team name", [validators.Required()])
	email = StringField("Email", [validators.Required()])
	organisation = StringField("Organisation")
	password = PasswordField("Password", [validators.Required(), validators.EqualTo("confirm", message="Passwords must match")])
	confirm = PasswordField("Repeat password")