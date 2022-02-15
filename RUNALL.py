import app.RUNTEST_APP
import MavicMaxGui.RUNTEST_GUI
import NodeCore.test_nodes.RUNTEST_NODE
import config

NodeCore.LOGDIR = config.test_settings.log_dir_test

def run():
    run_list=[
        app.RUNTEST_APP,
        NodeCore.test_nodes.RUNTEST_NODE,
        MavicMaxGui.RUNTEST_GUI
    ]
    for module in run_list:
        print(f'Running:{module.__name__}')
        func = module.run
        exitcode = func()
        if exitcode!=0: exit(1)



if __name__ == "__main__":
    run()

'''
TODO
Main loggar
Dir med Datum o tid för loggar
Se loggar i webläsare
Inga loggar när man kör main i app (på fel ställe)
Settingsfile som fixar alla dependencies, switch beroende på drönare eller desktop






Done
autostart
Nya noder:
 simulator
 git puller change branch
event -> buttons i view
Koppla view till menyn
Skapa view när en node startas
Automatiskt skapa gui element av input/output, en view till varje node.
Starta en node ifrån menyn
Clean up gui-code
Failsafe om man matar in ett icke nummer i in/ut fält.
Avrundning vid utskrift


Done
Fixa kill delete object. Nu raderas inte menyn
Fix meny med samma namn
Typer i gui element
read input fields with type

OLD
Klara lambda funktioner som test-input
Automatiskt köra runme vid incheck
rensa i init, tag bort all död kod.

terminera utifrån o sig själv.
Cascade terminering.
egen data som sparas mellan sessioner.
logs all logs in one file
exception i loops

generera noder från json fil, gömma icke användna in/ut signaler
generera execution order utifrån connect

Done
köra alla noder i ett filetree som test i RUNME
Göra det lättare att ta utdata som indata
automatsik generering av testdata.
chip enable, nix
sammanfattning antal passed/fail
Fixa till event i csv filer
Varna om det saknas input/output kolumner i csv filen

'''
