import yaml

with open('/home/saibot/git_repos/fit_programming_III/simulation_settings.yaml') as file:
    simulation_settings = yaml.load(file, Loader=yaml.FullLoader)

    print(simulation_settings)

print(simulation_settings['Bottom stem diameter x'])

