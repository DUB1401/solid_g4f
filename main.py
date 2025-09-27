from Source.Structs.Options import Options
from Source.Generators import Generate
from Source.Initializator import *

from dublib.CLI.Terminalyzer import Command, ParametersTypes, Terminalyzer
from dublib.Methods.Filesystem import WriteTextFile

import os

Commands = list()

Com = Command("init", "Create module files. Run after installation.")
Commands.append(Com)

Com = Command("generate", "Generate content.")
ComPos = Com.create_position("REQUEST", "Request text.", important = True)
Com.base.add_flag("proxy", "Force random proxy using.")
Com.base.add_key("language", ParametersTypes.Text, "Language code in ISO 639-1 format.")
Com.base.add_key("length", ParametersTypes.Number, "Max response length.")
Com.base.add_key("tries", ParametersTypes.Number, "Max generation tries.")
Com.base.add_key("timeout", ParametersTypes.Number, "Response generation timeout.")
Com.base.add_key("model", description = "Name of model.")
Com.base.add_key("source", description = "Generator source. Default to \"gpt4free\".")
Commands.append(Com)

Analyzer = Terminalyzer()
Analyzer.helper.enable()
CommandData = Analyzer.check_commands(Commands)

if not CommandData:
	print("Unknown command!")
	exit(-1)

match CommandData.name:

	case "init":
		if not os.path.exists("Proxies.txt"): WriteTextFile("Proxies.txt", "")
		# if not os.path.exists("har_and_cookies"): os.makedirs("har_and_cookies")

	case "generate":
		CurrentOptions = Options()
		
		CurrentOptions.set_force_proxy(CommandData.check_flag("proxy"))
		CurrentOptions.set_language(CommandData.get_key_value("language"))
		CurrentOptions.set_max_length(CommandData.get_key_value("length"))
		CurrentOptions.set_model(CommandData.get_key_value("model"))
		CurrentOptions.select_source(CommandData.get_key_value("source"))
		CurrentOptions.set_timeout(CommandData.get_key_value("timeout"))
		CurrentOptions.set_tries(CommandData.get_key_value("tries"))
		
		print(Generate(CommandData.arguments[0], CurrentOptions).to_dict())