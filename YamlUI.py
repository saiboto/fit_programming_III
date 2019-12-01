import yaml

def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath, data):
    with open (filepath, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)

if __name__== "__main__":
    filepath = "/home/saibot/git_repos/fit_programming_III/simulation_settings.yaml"
    data = yaml_loader(filepath)
    print data
    
    stem_settings = data.get('stem_settings')
    for stem_settings_name, stem_settings_value in stem_settings.iteritems():
        print stem_settings_name, stem_settings_value 



