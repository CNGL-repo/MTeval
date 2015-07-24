from wtforms import Form, StringField, PasswordField, DateTimeField, TextAreaField, FileField, validators

MIN_TEAM_NAME = 3
MAX_TEAM_NAME = 30
MIN_PASS = 6
MAX_PASS = 80


class LoginForm(Form):
	teamname = StringField("Team name", [validators.DataRequired("Team name / email required"), 
		validators.Length(min=MIN_TEAM_NAME, max=MAX_TEAM_NAME)])
	password = PasswordField("Password", [validators.DataRequired("Password required"), 
		validators.Length(min=MIN_PASS, max=MAX_PASS)])

class RegisterForm(Form):
	teamname = StringField("Team name", [validators.DataRequired("Team name required"), 
		validators.Length(min=MIN_TEAM_NAME, max=MAX_TEAM_NAME)])
	email = StringField("Email", [validators.DataRequired("Email required"),validators.Email()])
	organisation = StringField("Organisation")
	password = PasswordField("Password", [validators.DataRequired("Password required"), 
		validators.EqualTo("confirm", message="Passwords must match"), validators.Length(min=MIN_PASS, max=MAX_PASS)])
	confirm = PasswordField("Repeat password")

class EditTeamForm(Form):
	teamname = StringField("Team name", [validators.DataRequired("Team name required"),	validators.Length(min=MIN_TEAM_NAME, max=MAX_TEAM_NAME)])
	email = StringField("Email", [validators.DataRequired("Email required"),validators.Email()])
	organisation = StringField("Organisation")
	password = PasswordField("Change Password", [validators.DataRequired("Password required"), 
		validators.EqualTo("confirm", message="Passwords must match"), validators.Length(min=MIN_PASS, max=MAX_PASS)])
	confirm = PasswordField("Repeat password")

class CompetitionForm(Form):
	name = StringField("Competition Name", [validators.DataRequired("Competition name required")])
	description = StringField("Competition Description")
	deadline = DateTimeField("Deadline (dd/mm/yyyy hh:mm:ss)", format="%d/%m/%Y %H:%M:%S")
	submissionFormat = StringField("Format for submission")
	requirements = StringField("Requirements")
	organisers = TextAreaField("Organisers (one per line)")
	contact = StringField("Contact information")
	testData = FileField("Test Data")
	trainingData = FileField("Training Data")

class CompetitionEditForm(Form):
	name = StringField("Competition Name")
	description = StringField("Competition Description")
	deadline = DateTimeField("Deadline (dd/mm/yy hh:mm:ss)", format="%d/%m/%Y %H:%M:%S")
	submissionFormat = StringField("Format for submission")
	requirements = StringField("Requirements")
	organisers = TextAreaField("Organisers (one per line)")
	contact = StringField("Contact information")
	testData = FileField("Test Data")
	trainingData = FileField("Training Data")