
from jinja2 import Template

welcome_message = Template("Welcome {{name}}!")
message = welcome_message.render(name="Shweta")
print(message)

