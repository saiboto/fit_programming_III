import yaml


def yaml_loader(file_path):
    with open(file_path, "r") as file_descriptor:
        # The "FullLoader" is not mentioned in the documentation but there is a
        # wiki page about it on the package's github:
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load%28input%29-Deprecation
        return yaml.load(file_descriptor, Loader=yaml.FullLoader)


def yaml_dump(file_path, data):
    with open(file_path, "w") as file_descriptor:
        yaml.dump(data, file_descriptor)


if __name__ == "__main__":
    user_settings_file_path = "simulation_settings.yaml"
    user_settings = yaml_loader(user_settings_file_path)
    print(user_settings)

if __name__ == "__main__":
    user_settings_file_path = "simulation_settings.yaml"
    user_settings = yaml_loader(user_settings_file_path)
    print(user_settings)

    stem_settings = user_settings.get('Random stem generation')
    for stem_settings_name, stem_settings_value in stem_settings.items():
        print(stem_settings_name, stem_settings_value)
